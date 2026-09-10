"""Real-database tests for cross-visit history retrieval.

These run against SQLite rather than mocks, because the value of get_history
is entirely in the SQL it emits: the ordering, the soft-delete filtering, and
the query count. None of that is observable through a mocked session.

Only the visits and symptoms tables are created. Patient.__table__ is
deliberately left out -- it uses postgresql.ARRAY for allergies and cannot be
created on SQLite. SQLite accepts a REFERENCES patients(id) clause pointing at
a table that does not exist (foreign keys are off by default), so visits are
inserted with synthetic patient_id values.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from app.models.symptom import Symptom
from app.models.visit import Visit, VisitStatus
from app.repositories.visit_repository import VisitRepository


BASE_DATE = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)


def _engine():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Visit.__table__.create(engine)
    Symptom.__table__.create(engine)
    return engine


def _visit(patient_id, *, days_offset=0, complaint="tremor", symptoms=()):
    return Visit(
        patient_id=patient_id,
        visit_date=BASE_DATE + timedelta(days=days_offset),
        chief_complaint=complaint,
        vitals={},
        status=VisitStatus.DRAFT,
        symptoms=[
            Symptom(symptom_name=name, severity=severity)
            for name, severity in symptoms
        ],
    )


def test_history_returns_visits_newest_first_with_symptoms_attached() -> None:
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        db.add_all(
            [
                _visit(patient_id, days_offset=0, symptoms=[("tremor", 3)]),
                _visit(patient_id, days_offset=30, symptoms=[("tremor", 5)]),
                _visit(patient_id, days_offset=60, symptoms=[("tremor", 8)]),
            ]
        )
        db.commit()

        history = repository.get_history(db, patient_id)

        assert [visit.visit_date.day for visit in history] == [2, 31, 1]
        # The trend AI-01 needs to see: severity rising across visits.
        assert [visit.symptoms[0].severity for visit in history] == [8, 5, 3]


def test_history_can_be_returned_oldest_first() -> None:
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        db.add_all(
            [
                _visit(patient_id, days_offset=0, complaint="first"),
                _visit(patient_id, days_offset=10, complaint="second"),
            ]
        )
        db.commit()

        history = repository.get_history(db, patient_id, newest_first=False)

        assert [visit.chief_complaint for visit in history] == ["first", "second"]


def test_history_breaks_same_day_ties_by_creation_order() -> None:
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        earlier = _visit(patient_id, complaint="earlier")
        db.add(earlier)
        db.commit()

        later = _visit(patient_id, complaint="later")
        later.created_at = earlier.created_at + timedelta(seconds=1)
        db.add(later)
        db.commit()

        history = repository.get_history(db, patient_id)

        assert [visit.chief_complaint for visit in history] == ["later", "earlier"]


def test_history_honours_limit_and_excludes_the_current_visit() -> None:
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        visits = [_visit(patient_id, days_offset=day) for day in range(5)]
        db.add_all(visits)
        db.commit()
        current_id = visits[-1].id

        assert len(repository.get_history(db, patient_id, limit=2)) == 2

        remaining = repository.get_history(
            db, patient_id, exclude_visit_id=current_id
        )

        assert len(remaining) == 4
        assert current_id not in {visit.id for visit in remaining}


def test_history_scopes_to_one_patient() -> None:
    repository = VisitRepository()
    patient_id, other_patient_id = uuid4(), uuid4()

    with Session(_engine()) as db:
        db.add_all([_visit(patient_id), _visit(other_patient_id)])
        db.commit()

        history = repository.get_history(db, patient_id)

        assert len(history) == 1
        assert history[0].patient_id == patient_id


def test_history_omits_soft_deleted_visits() -> None:
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        live = _visit(patient_id, complaint="live")
        removed = _visit(patient_id, days_offset=1, complaint="removed")
        db.add_all([live, removed])
        db.commit()

        repository.soft_delete(db, removed)

        history = repository.get_history(db, patient_id)

        assert [visit.chief_complaint for visit in history] == ["live"]
        assert repository.count_by_patient(db, patient_id) == 1


def test_history_omits_soft_deleted_symptoms_from_eager_load() -> None:
    """The loader criteria, not just the read path, must filter soft deletes."""
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        visit = _visit(patient_id, symptoms=[("tremor", 4), ("aphasia", 6)])
        db.add(visit)
        db.commit()

        retracted = visit.symptoms[0]
        retracted.soft_delete()
        db.commit()
        db.expunge_all()

        history = repository.get_history(db, patient_id)

        assert [symptom.symptom_name for symptom in history[0].symptoms] == ["aphasia"]


def test_history_issues_two_queries_regardless_of_visit_count() -> None:
    """Regression guard for the N+1 the selectinload exists to prevent.

    One SELECT for the visits, one IN-clause SELECT for all their symptoms.
    A lazy-loading relationship would make this 1 + len(visits).
    """
    repository = VisitRepository()
    patient_id = uuid4()
    engine = _engine()

    with Session(engine) as db:
        db.add_all(
            [
                _visit(
                    patient_id,
                    days_offset=day,
                    symptoms=[(f"symptom-{index}", index + 1) for index in range(3)],
                )
                for day in range(5)
            ]
        )
        db.commit()
        db.expunge_all()

        selects = []

        @event.listens_for(engine, "before_cursor_execute")
        def _record(conn, cursor, statement, parameters, context, executemany):
            if statement.lstrip().upper().startswith("SELECT"):
                selects.append(statement)

        history = repository.get_history(db, patient_id)
        symptom_names = [
            symptom.symptom_name for visit in history for symptom in visit.symptoms
        ]

        event.remove(engine, "before_cursor_execute", _record)

    assert len(history) == 5
    assert len(symptom_names) == 15
    assert len(selects) == 2, f"expected 2 SELECTs, got {len(selects)}"


def test_get_by_patient_paginates_and_filters_by_status() -> None:
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        draft = _visit(patient_id, complaint="draft")
        closed = _visit(patient_id, days_offset=1, complaint="closed")
        closed.status = VisitStatus.CLOSED
        db.add_all([draft, closed])
        db.commit()

        assert repository.count_by_patient(db, patient_id) == 2
        assert (
            repository.count_by_patient(db, patient_id, status=VisitStatus.CLOSED) == 1
        )

        page = repository.get_by_patient(db, patient_id, skip=0, limit=1)
        assert [visit.chief_complaint for visit in page] == ["closed"]

        filtered = repository.get_by_patient(db, patient_id, status=VisitStatus.DRAFT)
        assert [visit.chief_complaint for visit in filtered] == ["draft"]


def test_get_with_symptoms_hides_soft_deleted_visits() -> None:
    repository = VisitRepository()
    patient_id = uuid4()

    with Session(_engine()) as db:
        visit = _visit(patient_id, symptoms=[("tremor", 2)])
        db.add(visit)
        db.commit()
        visit_id = visit.id

        assert repository.get_with_symptoms(db, visit_id) is not None

        repository.soft_delete(db, visit)

        assert repository.get_with_symptoms(db, visit_id) is None

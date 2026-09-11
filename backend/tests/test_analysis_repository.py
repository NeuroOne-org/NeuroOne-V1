"""Real-database tests for analysis persistence.

Run against SQLite because the value here is in the SQL: the atomicity of
create_with_status, the cascade, the eager-load, and the JSON round-trip that
proves the .with_variant(JSON(), "sqlite") columns actually work.

As in test_visit_repository.py, only the SQLite-creatable tables are built --
Patient uses postgresql.ARRAY for allergies and cannot be created here, and
SQLite accepts a dangling REFERENCES clause.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.analysis import (
    Analysis,
    AnalysisEvidence,
    AnalysisFinding,
    FindingCategory,
)
from app.models.symptom import Symptom
from app.models.visit import Visit, VisitStatus
from app.repositories.analysis_repository import AnalysisRepository
from app.utils.exceptions import DatabaseError


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


def _engine():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Visit.__table__.create(engine)
    Symptom.__table__.create(engine)
    Analysis.__table__.create(engine)
    AnalysisFinding.__table__.create(engine)
    AnalysisEvidence.__table__.create(engine)
    return engine


def _visit(patient_id=None):
    return Visit(
        id=uuid4(),
        patient_id=patient_id or uuid4(),
        visit_date=NOW,
        chief_complaint="tremor",
        vitals={},
        status=VisitStatus.SUBMITTED,
    )


def _evidence(rank=0):
    return AnalysisEvidence(
        rank=rank,
        source="Simulated Source",
        citation="Illustrative reference (simulated corpus), 2024.",
        relevant_passage="A passage.",
        document_id=f"doc-{rank}",
        chunk_id=f"doc-{rank}#c1",
        source_tier="guideline",
        published_year=2024,
        relevance_score=1.0,
    )


def _finding(rank=0, *, name="Condition A", category=None, evidence_count=1):
    return AnalysisFinding(
        rank=rank,
        condition_name=name,
        category=category or FindingCategory.DIFFERENTIAL_DIAGNOSIS,
        confidence=0.5,
        supporting_findings=["a finding"],
        contradicting_findings=[],
        explanation="an explanation",
        trend_basis=[],
        evidence=[_evidence(index) for index in range(evidence_count)],
    )


def _analysis(visit, *, findings=None, created_offset=0, snapshot=None):
    analysis = Analysis(
        visit_id=visit.id,
        requested_by_id=uuid4(),
        model_name="neuroone-mock-reasoner-v1",
        provider_mode="simulated",
        pipeline_note="pipeline complete, evidence retrieval simulated",
        disclaimer="Decision support only.",
        generated_at=NOW + timedelta(days=created_offset),
        context_snapshot=snapshot if snapshot is not None else {},
        findings=findings if findings is not None else [_finding()],
    )
    return analysis


# --------------------------------------------------------------------------
# Atomic write
# --------------------------------------------------------------------------


def test_create_with_status_commits_the_analysis_and_the_visit_together() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        visit = _visit()
        db.add(visit)
        db.commit()
        assert visit.status == VisitStatus.SUBMITTED

        stored = repository.create_with_status(db, _analysis(visit), visit)

        assert stored.id is not None
        assert db.get(Visit, visit.id).status == VisitStatus.ANALYZED
        assert repository.count_by_visit(db, visit.id) == 1


def test_a_failed_write_persists_neither_half() -> None:
    """AGENTS.md 8.5: a failure must not leave the record partly changed."""
    repository = AnalysisRepository()
    engine = _engine()

    with Session(engine) as db:
        visit = _visit()
        db.add(visit)
        db.commit()
        visit_id = visit.id

        def _fail():
            db.flush()
            raise SQLAlchemyError("write failed")

        db.commit = _fail

        with pytest.raises(DatabaseError):
            repository.create_with_status(db, _analysis(visit), visit)

    with Session(engine) as verify:
        assert verify.scalar(select(Analysis)) is None
        assert verify.get(Visit, visit_id).status == VisitStatus.SUBMITTED


def test_rollback_is_requested_on_failure() -> None:
    repository = AnalysisRepository()
    db = Mock()
    db.commit.side_effect = SQLAlchemyError("boom")

    with pytest.raises(DatabaseError):
        repository.create_with_status(db, Mock(), Mock())

    db.rollback.assert_called_once_with()


# --------------------------------------------------------------------------
# Graph, cascade and JSON round-trip
# --------------------------------------------------------------------------


def test_findings_and_evidence_are_persisted_in_rank_order() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        analysis = _analysis(
            visit,
            findings=[
                _finding(0, name="First", evidence_count=2),
                _finding(1, name="Second", evidence_count=1),
            ],
        )
        stored = repository.create_with_status(db, analysis, visit)
        db.expunge_all()

        loaded = repository.get_with_graph(db, stored.id)

        assert [f.condition_name for f in loaded.findings] == ["First", "Second"]
        assert [len(f.evidence) for f in loaded.findings] == [2, 1]
        assert [e.rank for e in loaded.findings[0].evidence] == [0, 1]


def test_trend_basis_and_context_snapshot_survive_a_json_round_trip() -> None:
    """Proves the .with_variant(JSON(), "sqlite") columns work as intended."""
    repository = AnalysisRepository()
    visit_ref, symptom_ref = str(uuid4()), str(uuid4())
    trend_basis = [
        {
            "visit_id": visit_ref,
            "symptom_id": symptom_ref,
            "symptom_name": "memory loss",
            "severity": 4,
            "observation": "memory loss severity 2 -> 4 across 3 visits",
        }
    ]
    snapshot = {"patient_age_years": 62, "trends": [{"direction": "worsening"}]}

    with Session(_engine()) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        finding = _finding(0, category=FindingCategory.EARLY_WATCH)
        finding.trend_basis = trend_basis
        stored = repository.create_with_status(
            db, _analysis(visit, findings=[finding], snapshot=snapshot), visit
        )
        db.expunge_all()

        loaded = repository.get_with_graph(db, stored.id)

        assert loaded.context_snapshot == snapshot
        assert loaded.findings[0].trend_basis == trend_basis
        assert loaded.findings[0].category == FindingCategory.EARLY_WATCH


def test_deleting_an_analysis_cascades_to_findings_and_evidence() -> None:
    repository = AnalysisRepository()
    engine = _engine()

    with Session(engine) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        stored = repository.create_with_status(
            db, _analysis(visit, findings=[_finding(0, evidence_count=2)]), visit
        )
        db.delete(stored)
        db.commit()

    with Session(engine) as verify:
        assert verify.scalar(select(AnalysisFinding)) is None
        assert verify.scalar(select(AnalysisEvidence)) is None


def test_soft_deleted_findings_are_excluded_from_the_eager_load() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        stored = repository.create_with_status(
            db,
            _analysis(
                visit,
                findings=[_finding(0, name="live"), _finding(1, name="retracted")],
            ),
            visit,
        )
        analysis_id = stored.id
        stored.findings[1].soft_delete()
        db.commit()
        db.expunge_all()

        loaded = repository.get_with_graph(db, analysis_id)

        assert [f.condition_name for f in loaded.findings] == ["live"]


def test_loading_an_analysis_graph_issues_a_bounded_number_of_queries() -> None:
    """Guards the eager load: one analysis, one findings, one evidence."""
    repository = AnalysisRepository()
    engine = _engine()

    with Session(engine) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        stored = repository.create_with_status(
            db,
            _analysis(
                visit,
                findings=[
                    _finding(index, name=f"C{index}", evidence_count=2)
                    for index in range(4)
                ],
            ),
            visit,
        )
        analysis_id = stored.id
        db.expunge_all()

        selects = []

        @event.listens_for(engine, "before_cursor_execute")
        def _record(conn, cursor, statement, parameters, context, executemany):
            if statement.lstrip().upper().startswith("SELECT"):
                selects.append(statement)

        loaded = repository.get_with_graph(db, analysis_id)
        citations = [e.citation for f in loaded.findings for e in f.evidence]

        event.remove(engine, "before_cursor_execute", _record)

    assert len(citations) == 8
    assert len(selects) == 3, f"expected 3 SELECTs, got {len(selects)}"


# --------------------------------------------------------------------------
# Lookups
# --------------------------------------------------------------------------


def test_latest_returns_the_most_recent_analysis() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        first = repository.create_with_status(
            db, _analysis(visit, findings=[_finding(0, name="older")]), visit
        )
        second = _analysis(visit, findings=[_finding(0, name="newer")])
        second.created_at = first.created_at + timedelta(seconds=1)
        stored_second = repository.create_with_status(db, second, visit)

        latest = repository.get_latest_by_visit(db, visit.id)

        assert latest.id == stored_second.id
        assert latest.findings[0].condition_name == "newer"
        assert repository.count_by_visit(db, visit.id) == 2


def test_rerunning_analysis_does_not_overwrite_the_previous_run() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        repository.create_with_status(db, _analysis(visit), visit)
        repository.create_with_status(db, _analysis(visit), visit)

        assert len(repository.get_by_visit(db, visit.id)) == 2


def test_analyses_are_scoped_to_their_visit() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        visit, other = _visit(), _visit()
        db.add_all([visit, other])
        db.commit()

        repository.create_with_status(db, _analysis(visit), visit)

        assert repository.count_by_visit(db, other.id) == 0
        assert repository.get_latest_by_visit(db, other.id) is None


def test_soft_deleted_analyses_are_hidden() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        visit = _visit()
        db.add(visit)
        db.commit()

        stored = repository.create_with_status(db, _analysis(visit), visit)
        repository.soft_delete(db, stored)

        assert repository.get_with_graph(db, stored.id) is None
        assert repository.count_by_visit(db, visit.id) == 0


# --------------------------------------------------------------------------
# Latest-per-patient (triage queue, ADR-006)
# --------------------------------------------------------------------------


def test_get_latest_by_patient_ids_with_no_ids_returns_empty() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        assert repository.get_latest_by_patient_ids(db, []) == {}


def test_get_latest_by_patient_ids_picks_each_patients_most_recent_analysis() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        patient_a, patient_b = uuid4(), uuid4()
        visit_a1, visit_a2 = _visit(patient_a), _visit(patient_a)
        visit_b1 = _visit(patient_b)
        db.add_all([visit_a1, visit_a2, visit_b1])
        db.commit()

        older_a = repository.create_with_status(
            db, _analysis(visit_a1, findings=[_finding(0, name="older-a")]), visit_a1
        )
        newer_a = _analysis(visit_a2, findings=[_finding(0, name="newer-a")])
        newer_a.created_at = older_a.created_at + timedelta(seconds=1)
        stored_newer_a = repository.create_with_status(db, newer_a, visit_a2)

        only_b = repository.create_with_status(
            db, _analysis(visit_b1, findings=[_finding(0, name="only-b")]), visit_b1
        )

        latest = repository.get_latest_by_patient_ids(db, [patient_a, patient_b])

        assert latest[patient_a].id == stored_newer_a.id
        assert latest[patient_a].findings[0].condition_name == "newer-a"
        assert latest[patient_b].id == only_b.id


def test_get_latest_by_patient_ids_ignores_soft_deleted_analyses() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        patient = uuid4()
        visit = _visit(patient)
        db.add(visit)
        db.commit()

        first = repository.create_with_status(
            db, _analysis(visit, findings=[_finding(0, name="kept")]), visit
        )
        deleted = _analysis(visit, findings=[_finding(0, name="retracted")])
        deleted.created_at = first.created_at + timedelta(seconds=1)
        stored_deleted = repository.create_with_status(db, deleted, visit)
        repository.soft_delete(db, stored_deleted)

        latest = repository.get_latest_by_patient_ids(db, [patient])

        assert latest[patient].id == first.id


def test_get_latest_by_patient_ids_omits_patients_with_no_analysis() -> None:
    repository = AnalysisRepository()

    with Session(_engine()) as db:
        analyzed_patient, unanalyzed_patient = uuid4(), uuid4()
        visit = _visit(analyzed_patient)
        db.add(visit)
        db.commit()
        repository.create_with_status(db, _analysis(visit), visit)

        latest = repository.get_latest_by_patient_ids(
            db, [analyzed_patient, unanalyzed_patient]
        )

        assert analyzed_patient in latest
        assert unanalyzed_patient not in latest

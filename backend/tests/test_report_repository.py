"""Real-database tests for report persistence.

Runs against SQLite because the value here is in the SQL: soft-delete
filtering, analysis-scoped listing, and the snapshot JSON round-trip that
proves the .with_variant(JSON(), "sqlite") column actually works. Only the
reports table is created -- SQLite has foreign keys off by default, so a
REFERENCES clause pointing at analyses/users can stay dangling, exactly as
test_visit_repository.py already relies on for patients.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.report import Report
from app.repositories.report_repository import ReportRepository


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


def _engine():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Report.__table__.create(engine)
    return engine


def _snapshot(**overrides) -> dict:
    payload = {
        "analysis_id": str(uuid4()),
        "patient": {"full_name": "Ada Lovelace"},
        "findings": [{"condition_name": "Essential tremor"}],
    }
    payload.update(overrides)
    return payload


def _report(analysis_id=None, *, generated_offset=0, snapshot=None) -> Report:
    return Report(
        analysis_id=analysis_id or uuid4(),
        generated_by_id=uuid4(),
        generated_at=NOW + timedelta(days=generated_offset),
        filename="neuroone-report-placeholder.pdf",
        snapshot=snapshot if snapshot is not None else _snapshot(),
    )


def test_a_report_is_created_and_retrieved_by_id() -> None:
    repository = ReportRepository()

    with Session(_engine()) as db:
        report = repository.create(db, _report())

        assert report.id is not None
        loaded = repository.get_by_id(db, report.id)
        assert loaded is not None
        assert loaded.filename == "neuroone-report-placeholder.pdf"


def test_the_snapshot_survives_a_json_round_trip() -> None:
    """Proves the .with_variant(JSON(), "sqlite") column works as intended."""
    repository = ReportRepository()
    snapshot = _snapshot(patient={"full_name": "Grace Hopper", "age_years": 62})

    with Session(_engine()) as db:
        stored = repository.create(db, _report(snapshot=snapshot))
        db.expunge_all()

        loaded = repository.get_by_id(db, stored.id)

        assert loaded.snapshot == snapshot


def test_reports_are_scoped_to_their_analysis() -> None:
    repository = ReportRepository()
    analysis_id, other_id = uuid4(), uuid4()

    with Session(_engine()) as db:
        repository.create(db, _report(analysis_id))
        repository.create(db, _report(analysis_id, generated_offset=1))
        repository.create(db, _report(other_id))

        reports = repository.get_by_analysis(db, analysis_id)

        assert len(reports) == 2
        assert repository.count_by_analysis(db, analysis_id) == 2
        assert repository.count_by_analysis(db, other_id) == 1


def test_reports_are_listed_newest_first() -> None:
    repository = ReportRepository()
    analysis_id = uuid4()

    with Session(_engine()) as db:
        first = repository.create(db, _report(analysis_id, generated_offset=0))
        second = repository.create(db, _report(analysis_id, generated_offset=1))
        second.created_at = first.created_at + timedelta(seconds=1)
        db.commit()

        reports = repository.get_by_analysis(db, analysis_id)

        assert reports[0].id == second.id
        assert reports[1].id == first.id


def test_regenerating_a_report_does_not_overwrite_the_previous_one() -> None:
    """ADR-004: multiple reports per analysis are permitted; none are mutated."""
    repository = ReportRepository()
    analysis_id = uuid4()

    with Session(_engine()) as db:
        repository.create(db, _report(analysis_id))
        repository.create(db, _report(analysis_id))

        assert repository.count_by_analysis(db, analysis_id) == 2


def test_soft_deleted_reports_are_hidden() -> None:
    repository = ReportRepository()

    with Session(_engine()) as db:
        report = repository.create(db, _report())
        repository.soft_delete(db, report)

        assert repository.get_by_id(db, report.id) is None
        assert repository.count_by_analysis(db, report.analysis_id) == 0

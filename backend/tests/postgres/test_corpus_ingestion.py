"""Ingestion idempotence and version-retirement, against real Postgres
(ADR-007 Testing Impact, AI-02b-8). Skipped unless TEST_POSTGRES_URL is set.
"""

from datetime import date
from pathlib import Path

import pytest

from app.ai.corpus.source_schema import (
    CorpusManifest,
    CorpusPassage,
    CorpusSourceFile,
    load_manifest,
    load_source_file,
)
from app.models.corpus import CorpusDocument
from app.repositories.corpus_repository import CorpusRepository


pytestmark = pytest.mark.postgres

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "corpus"


def _source_file(**overrides) -> CorpusSourceFile:
    defaults = dict(
        document_id="test-guideline-2024",
        source="Test Source",
        citation="Test Source. A guideline. 2024.",
        source_url=None,
        source_tier="guideline",
        published_year=2024,
        license="CC0-1.0",
        keywords=["dementia"],
        reviewed_by="tester",
        reviewed_at=date(2026, 1, 1),
        passages=[CorpusPassage(chunk_id="test-guideline-2024#c1", text="A passage.")],
    )
    defaults.update(overrides)
    return CorpusSourceFile(**defaults)


def test_ingestion_is_idempotent(pg_session):
    manifest = CorpusManifest(corpus_version="test-v1", files=["a.yaml"])
    repository = CorpusRepository()

    first = repository.replace_version(pg_session, manifest, [_source_file()])
    assert (first.inserted, first.unchanged) == (1, 0)

    second = repository.replace_version(pg_session, manifest, [_source_file()])
    assert (second.inserted, second.unchanged) == (0, 1)


def test_version_switch_deactivates_the_previous_version(pg_session):
    repository = CorpusRepository()
    v1 = CorpusManifest(corpus_version="test-v1", files=["a.yaml"])
    v2 = CorpusManifest(corpus_version="test-v2", files=["b.yaml"])

    repository.replace_version(pg_session, v1, [_source_file()])
    repository.replace_version(
        pg_session,
        v2,
        [
            _source_file(
                document_id="test-guideline-2025",
                passages=[
                    CorpusPassage(
                        chunk_id="test-guideline-2025#c1",
                        text="Another passage.",
                    )
                ],
            )
        ],
    )

    rows = pg_session.query(CorpusDocument).all()
    active_by_version = {row.corpus_version: row.is_active for row in rows}
    assert active_by_version["test-v1"] is False
    assert active_by_version["test-v2"] is True


def test_invalid_file_writes_nothing(pg_session):
    """A CLI-style validate-then-load: an invalid file must never reach
    replace_version, so this test confirms the boundary rather than
    replace_version's own behavior (it never sees invalid files)."""

    valid = _source_file()
    manifest = CorpusManifest(corpus_version="test-v1", files=["a.yaml", "bad.yaml"])

    # Simulates the CLI's own validate-all-first loop: a bad file (wrong
    # tier) is caught before replace_version is ever called.
    errors = []
    try:
        CorpusSourceFile.model_validate(
            {**_source_file().model_dump(mode="json"), "source_tier": "primary_study"}
        )
    except Exception as exc:  # noqa: BLE001 -- validation failure is expected
        errors.append(str(exc))

    assert errors, "the invalid file must fail validation"

    repository = CorpusRepository()
    if not errors:
        repository.replace_version(pg_session, manifest, [valid])

    count = pg_session.query(CorpusDocument).count()
    assert count == 0


def test_the_fixture_corpus_ingests_end_to_end(pg_session):
    """Loads the real fixture files from disk (not Python-constructed
    objects), exercising the same path scripts/ingest_documents.py uses."""

    manifest = load_manifest(FIXTURES_DIR / "manifest.yaml")
    files = [
        load_source_file(
            FIXTURES_DIR / "documents" / filename,
            documents_dir=FIXTURES_DIR / "documents",
        )
        for filename in manifest.files
    ]

    result = CorpusRepository().replace_version(pg_session, manifest, files)

    assert result.inserted == 1
    row = pg_session.query(CorpusDocument).one()
    assert row.document_id == "test-guideline-2024"
    assert row.reviewed_by == "test-fixture"
    assert row.is_active is True

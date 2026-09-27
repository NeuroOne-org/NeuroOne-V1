"""Real-SQL tests for CorpusRepository and the corpus_documents migration
(ADR-007 Testing Impact, AI-02b-8). Skipped unless TEST_POSTGRES_URL is set.
"""

import uuid
from datetime import date

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.ai.providers.base import CorpusSearchTerms
from app.models.corpus import CorpusDocument
from app.repositories.corpus_repository import CorpusRepository


pytestmark = pytest.mark.postgres

ALLOWED_TIERS = frozenset({"guideline", "systematic_review"})


def _row(db, **overrides) -> CorpusDocument:
    document_id = overrides.pop("document_id", f"doc-{uuid.uuid4().hex[:8]}")
    defaults = dict(
        document_id=document_id,
        chunk_id=f"{document_id}#c1",
        source="Test Source",
        citation="Test Source. A guideline. 2024.",
        relevant_passage="A passage about the condition.",
        source_url=None,
        source_tier="guideline",
        published_year=2024,
        keywords="dementia;memory loss",
        corpus_version="test-v1",
        content_sha256="0" * 64,
        license="CC0-1.0",
        reviewed_by="tester",
        reviewed_at=date(2026, 1, 1),
        is_active=True,
    )
    defaults.update(overrides)
    row = CorpusDocument(**defaults)
    db.add(row)
    db.flush()
    return row


def test_migration_creates_the_generated_search_vector_and_gin_index(pg_session):
    column = pg_session.execute(
        text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'corpus_documents' AND column_name = 'search_vector'"
        )
    ).first()
    assert column is not None

    index = pg_session.execute(
        text(
            "SELECT indexdef FROM pg_indexes WHERE tablename = 'corpus_documents' "
            "AND indexname = 'ix_corpus_documents_search_vector'"
        )
    ).first()
    assert index is not None
    assert "gin" in index[0].lower()


def test_check_constraint_rejects_a_disallowed_tier(pg_session):
    # _row() itself flushes, and the CHECK constraint fires on flush, not
    # only on commit -- so the assertion has to wrap the call that actually
    # touches the database, not a separate commit() afterward.
    with pytest.raises(IntegrityError):
        _row(pg_session, source_tier="primary_study")
    pg_session.rollback()


def test_ranking_prioritizes_condition_then_symptom_then_complaint(pg_session):
    _row(
        pg_session,
        document_id="doc-condition-match",
        keywords="parkinsonian syndrome",
        relevant_passage="Neutral passage text.",
    )
    _row(
        pg_session,
        document_id="doc-symptom-match",
        keywords="resting tremor",
        relevant_passage="Neutral passage text.",
    )
    pg_session.commit()

    hits = CorpusRepository().search(
        pg_session,
        CorpusSearchTerms(
            conditions=("parkinsonian syndrome",),
            symptoms=("resting tremor",),
            complaint_terms=(),
        ),
        tiers=ALLOWED_TIERS,
        limit=10,
    )

    assert [hit.document_id for hit in hits[:2]] == [
        "doc-condition-match",
        "doc-symptom-match",
    ]


def test_inactive_rows_are_never_returned(pg_session):
    _row(pg_session, document_id="doc-inactive", keywords="dementia", is_active=False)
    _row(pg_session, document_id="doc-active", keywords="dementia", is_active=True)
    pg_session.commit()

    hits = CorpusRepository().search(
        pg_session,
        CorpusSearchTerms(conditions=("dementia",), symptoms=(), complaint_terms=()),
        tiers=ALLOWED_TIERS,
        limit=10,
    )

    ids = [hit.document_id for hit in hits]
    assert "doc-inactive" not in ids
    assert "doc-active" in ids


def test_limit_is_honoured(pg_session):
    for index in range(5):
        _row(pg_session, document_id=f"doc-{index}", keywords="dementia")
    pg_session.commit()

    hits = CorpusRepository().search(
        pg_session,
        CorpusSearchTerms(conditions=("dementia",), symptoms=(), complaint_terms=()),
        tiers=ALLOWED_TIERS,
        limit=2,
    )

    assert len(hits) == 2


@pytest.mark.parametrize(
    "hostile",
    [
        "memory & !loss | ') ; DROP TABLE corpus_documents; --",
        "dementia' OR '1'='1",
        "(unbalanced & parens",
    ],
)
def test_hostile_query_text_never_raises_or_executes(pg_session, hostile):
    """plainto_tsquery treats input as plain text, never tsquery syntax, and
    every value is a bound parameter -- so hostile text is inert (ADR-007
    decision 6, Security/Privacy Impact)."""

    _row(pg_session, document_id="doc-safe", keywords="dementia")
    pg_session.commit()

    CorpusRepository().search(
        pg_session,
        CorpusSearchTerms(conditions=(), symptoms=(), complaint_terms=(hostile,)),
        tiers=ALLOWED_TIERS,
        limit=10,
    )

    # The injection attempt did not execute: the table still exists and the
    # row inserted above is still there.
    count = pg_session.execute(
        text("SELECT count(*) FROM corpus_documents")
    ).scalar()
    assert count == 1

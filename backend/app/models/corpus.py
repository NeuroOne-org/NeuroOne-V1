"""Curated retrieval-corpus storage (ADR-007 decision 2).

One row per reviewed passage. `search_vector` -- the generated Postgres
`tsvector` column the migration creates for full-text search -- is
deliberately absent from this model: it is Postgres-only DDL, created and
indexed directly by the migration, and `alembic/env.py`'s `include_object`
hook excludes it from autogenerate so SQLite (the fast test suite's engine)
never has to represent a type it does not support.

Not a `BaseModel` subclass: versioning here is `corpus_version` /
`is_active`, not soft-delete, and a retired version's rows are kept for
traceability rather than marked deleted (`analysis_evidence` already copies
the fields it needs at analysis time, so nothing downstream depends on this
table's history staying queryable).
"""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    UUID,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CorpusDocument(Base):
    """One reviewed passage of curated literature, unique per (document_id, chunk_id)."""

    __tablename__ = "corpus_documents"
    __table_args__ = (
        CheckConstraint(
            "source_tier IN ('guideline', 'systematic_review')",
            name="ck_corpus_documents_source_tier",
        ),
        UniqueConstraint(
            "document_id",
            "chunk_id",
            name="uq_corpus_documents_document_id_chunk_id",
        ),
        Index(
            "ix_corpus_documents_is_active_source_tier",
            "is_active",
            "source_tier",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    document_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    chunk_id: Mapped[str] = mapped_column(String(100), nullable=False)

    source: Mapped[str] = mapped_column(String(255), nullable=False)
    citation: Mapped[str] = mapped_column(String(500), nullable=False)
    relevant_passage: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_tier: Mapped[str] = mapped_column(String(30), nullable=False)
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # `;`-joined, not an array: the generated search_vector expression must
    # be immutable, and Postgres has no immutable array-to-text path.
    # `RetrievedDocument.keywords` is a tuple; the retriever splits this
    # back apart on the way out.
    keywords: Mapped[str] = mapped_column(Text, nullable=False, default="")

    corpus_version: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    license: Mapped[str] = mapped_column(String(40), nullable=False)
    reviewed_by: Mapped[str] = mapped_column(String(255), nullable=False)
    reviewed_at: Mapped[date] = mapped_column(Date, nullable=False)

    # True only for the rows of the manifest's active corpus_version. A
    # version switch flips this for every affected row in one transaction
    # (CorpusRepository.replace_version) rather than deleting anything.
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


__all__ = ["CorpusDocument"]

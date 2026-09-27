"""create corpus_documents

Revision ID: 9bfef8b66969
Revises: e3a91c5d7f20
Create Date: 2026-09-22

ADR-007: one additive table backing the curated retrieval corpus. No
existing table changes. Downgrade drops the table cleanly -- nothing
references it by foreign key, and `analysis_evidence` rows already carry
copies of the metadata they need, so dropping it loses no analysis history.

`search_vector` (Postgres full-text search) is added and indexed with raw
SQL, guarded to the postgresql dialect, because it is a generated `tsvector`
column that SQLite (the fast test suite's engine) cannot represent. It is
never declared on the `CorpusDocument` ORM model for the same reason;
`alembic/env.py`'s `include_object` hook keeps autogenerate from proposing
to drop it.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9bfef8b66969"
down_revision: Union[str, Sequence[str], None] = "e3a91c5d7f20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "corpus_documents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("document_id", sa.String(length=100), nullable=False),
        sa.Column("chunk_id", sa.String(length=100), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("citation", sa.String(length=500), nullable=False),
        sa.Column("relevant_passage", sa.Text(), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("source_tier", sa.String(length=30), nullable=False),
        sa.Column("published_year", sa.Integer(), nullable=True),
        sa.Column("keywords", sa.Text(), nullable=False),
        sa.Column("corpus_version", sa.String(length=40), nullable=False),
        sa.Column("content_sha256", sa.String(length=64), nullable=False),
        sa.Column("license", sa.String(length=40), nullable=False),
        sa.Column("reviewed_by", sa.String(length=255), nullable=False),
        sa.Column("reviewed_at", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "source_tier IN ('guideline', 'systematic_review')",
            name=op.f("ck_corpus_documents_source_tier"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_corpus_documents")),
        sa.UniqueConstraint(
            "document_id",
            "chunk_id",
            name=op.f("uq_corpus_documents_document_id_chunk_id"),
        ),
    )
    op.create_index(
        op.f("ix_corpus_documents_document_id"),
        "corpus_documents",
        ["document_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_corpus_documents_corpus_version"),
        "corpus_documents",
        ["corpus_version"],
        unique=False,
    )
    op.create_index(
        "ix_corpus_documents_is_active_source_tier",
        "corpus_documents",
        ["is_active", "source_tier"],
        unique=False,
    )

    if op.get_bind().dialect.name == "postgresql":
        # A STORED generated column: weights keywords (A), citation (B) and
        # the passage itself (C) under the `english` text-search
        # configuration (ADR-007 decision 2 / decision 6 ranking weights).
        op.execute(
            """
            ALTER TABLE corpus_documents
            ADD COLUMN search_vector tsvector GENERATED ALWAYS AS (
                setweight(to_tsvector('english', coalesce(keywords, '')), 'A')
                || setweight(to_tsvector('english', citation), 'B')
                || setweight(to_tsvector('english', relevant_passage), 'C')
            ) STORED
            """
        )
        op.create_index(
            "ix_corpus_documents_search_vector",
            "corpus_documents",
            ["search_vector"],
            unique=False,
            postgresql_using="gin",
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        op.drop_index("ix_corpus_documents_search_vector", table_name="corpus_documents")

    op.drop_index(
        "ix_corpus_documents_is_active_source_tier", table_name="corpus_documents"
    )
    op.drop_index(
        op.f("ix_corpus_documents_corpus_version"), table_name="corpus_documents"
    )
    op.drop_index(
        op.f("ix_corpus_documents_document_id"), table_name="corpus_documents"
    )
    op.drop_table("corpus_documents")

"""create analyses, findings and evidence

Revision ID: c4e19a7b6d20
Revises: b8d41e2f7c53
Create Date: 2026-09-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c4e19a7b6d20"
down_revision: Union[str, Sequence[str], None] = "b8d41e2f7c53"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# SQLEnum persists member NAMES, not values, so the type is declared with the
# uppercase members -- matching the visitstatus precedent in a3c7be51d904.
finding_category = sa.Enum(
    "DIFFERENTIAL_DIAGNOSIS",
    "EARLY_WATCH",
    name="findingcategory",
)


def upgrade() -> None:
    """Create the AI analysis tables.

    No drops. The abandoned Diagnosis and Rag stubs were never created by any
    migration -- they were unreferenced Python, not live schema -- so there is
    nothing to remove here.
    """

    op.create_table(
        "analyses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("visit_id", sa.UUID(), nullable=False),
        sa.Column("requested_by_id", sa.UUID(), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("provider_mode", sa.String(length=20), nullable=False),
        sa.Column("pipeline_note", sa.Text(), nullable=False),
        sa.Column("disclaimer", sa.Text(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "context_snapshot",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
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
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["visit_id"],
            ["visits.id"],
            name=op.f("fk_analyses_visit_id_visits"),
        ),
        sa.ForeignKeyConstraint(
            ["requested_by_id"],
            ["users.id"],
            name=op.f("fk_analyses_requested_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analyses")),
    )
    op.create_index(
        op.f("ix_analyses_visit_id"),
        "analyses",
        ["visit_id"],
        unique=False,
    )
    op.create_index(
        "ix_analyses_visit_created",
        "analyses",
        ["visit_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "analysis_findings",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("analysis_id", sa.UUID(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("condition_name", sa.String(length=200), nullable=False),
        sa.Column("category", finding_category, nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column(
            "supporting_findings",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "contradicting_findings",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column(
            "trend_basis",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
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
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name=op.f("ck_analysis_findings_confidence_range"),
        ),
        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["analyses.id"],
            name=op.f("fk_analysis_findings_analysis_id_analyses"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_findings")),
        sa.UniqueConstraint(
            "analysis_id",
            "rank",
            name=op.f("uq_analysis_findings_analysis_id"),
        ),
    )
    op.create_index(
        op.f("ix_analysis_findings_analysis_id"),
        "analysis_findings",
        ["analysis_id"],
        unique=False,
    )

    op.create_table(
        "analysis_evidence",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("finding_id", sa.UUID(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("citation", sa.String(length=500), nullable=False),
        sa.Column("relevant_passage", sa.Text(), nullable=False),
        sa.Column("document_id", sa.String(length=100), nullable=True),
        sa.Column("chunk_id", sa.String(length=100), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("source_tier", sa.String(length=30), nullable=True),
        sa.Column("published_year", sa.Integer(), nullable=True),
        sa.Column("relevance_score", sa.Float(), nullable=True),
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
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["finding_id"],
            ["analysis_findings.id"],
            name=op.f("fk_analysis_evidence_finding_id_analysis_findings"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_evidence")),
    )
    op.create_index(
        op.f("ix_analysis_evidence_finding_id"),
        "analysis_evidence",
        ["finding_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the analysis tables and the enum type they created."""

    op.drop_index(
        op.f("ix_analysis_evidence_finding_id"), table_name="analysis_evidence"
    )
    op.drop_table("analysis_evidence")

    op.drop_index(
        op.f("ix_analysis_findings_analysis_id"), table_name="analysis_findings"
    )
    op.drop_table("analysis_findings")

    op.drop_index("ix_analyses_visit_created", table_name="analyses")
    op.drop_index(op.f("ix_analyses_visit_id"), table_name="analyses")
    op.drop_table("analyses")

    # Postgres does not drop an enum type when the table using it is dropped,
    # so without this the next upgrade fails with "type already exists".
    finding_category.drop(op.get_bind(), checkfirst=True)

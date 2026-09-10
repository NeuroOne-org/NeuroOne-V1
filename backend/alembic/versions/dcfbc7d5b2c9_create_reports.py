"""create reports

Revision ID: dcfbc7d5b2c9
Revises: b2b31bad27df
Create Date: 2026-09-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "dcfbc7d5b2c9"
down_revision: Union[str, Sequence[str], None] = "b2b31bad27df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the reports table (ADR-004).

    No pdf_path and no binary PDF column: only the typed snapshot a download
    re-renders from is persisted.
    """

    op.create_table(
        "reports",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("analysis_id", sa.UUID(), nullable=False),
        sa.Column("generated_by_id", sa.UUID(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("filename", sa.String(length=100), nullable=False),
        sa.Column(
            "snapshot",
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
            ["analysis_id"],
            ["analyses.id"],
            name=op.f("fk_reports_analysis_id_analyses"),
        ),
        sa.ForeignKeyConstraint(
            ["generated_by_id"],
            ["users.id"],
            name=op.f("fk_reports_generated_by_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reports")),
    )
    op.create_index(
        op.f("ix_reports_analysis_id"),
        "reports",
        ["analysis_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the reports table."""

    op.drop_index(op.f("ix_reports_analysis_id"), table_name="reports")
    op.drop_table("reports")

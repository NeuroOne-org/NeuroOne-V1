"""add analysis sign-off

Revision ID: 7544ad0b1ed6
Revises: 14056b8ec27d
Create Date: 2026-09-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7544ad0b1ed6"
down_revision: Union[str, Sequence[str], None] = "14056b8ec27d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add clinician sign-off columns to analyses (ADR-006 decision 6).

    Both nullable and both null until a clinician reviews the analysis --
    ReportService.generate_report refuses to run while reviewed_at is null.
    """

    op.add_column("analyses", sa.Column("reviewed_by_id", sa.UUID(), nullable=True))
    op.add_column(
        "analyses",
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        op.f("fk_analyses_reviewed_by_id_users"),
        "analyses",
        "users",
        ["reviewed_by_id"],
        ["id"],
    )


def downgrade() -> None:
    """Drop the sign-off columns."""

    op.drop_constraint(
        op.f("fk_analyses_reviewed_by_id_users"), "analyses", type_="foreignkey"
    )
    op.drop_column("analyses", "reviewed_at")
    op.drop_column("analyses", "reviewed_by_id")

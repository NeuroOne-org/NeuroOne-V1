"""add symptom observation

Revision ID: b2b31bad27df
Revises: c4e19a7b6d20
Create Date: 2026-09-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b2b31bad27df"
down_revision: Union[str, Sequence[str], None] = "c4e19a7b6d20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the clinician-entered observation field (FR-03).

    Nullable, so every existing symptom row remains valid without a backfill.
    """

    op.add_column(
        "symptoms",
        sa.Column("observation", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    """Drop the observation column."""

    op.drop_column("symptoms", "observation")

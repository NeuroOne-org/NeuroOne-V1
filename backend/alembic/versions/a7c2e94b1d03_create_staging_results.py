"""create staging_results

Revision ID: a7c2e94b1d03
Revises: 9bfef8b66969
Create Date: 2026-10-12

One additive table persisting imaging-staging results per (checksum,
model_name), replacing the live stager's per-process cache (ADR-008 risk).
Nothing references it, so downgrade drops it cleanly; the only loss is that
scans get staged again on their next analysis.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "a7c2e94b1d03"
down_revision: Union[str, Sequence[str], None] = "9bfef8b66969"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "staging_results",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column(
            "result",
            postgresql.JSONB().with_variant(sa.JSON(), "sqlite"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_staging_results")),
        sa.UniqueConstraint(
            "checksum",
            "model_name",
            name=op.f("uq_staging_results_checksum"),
        ),
    )


def downgrade() -> None:
    op.drop_table("staging_results")

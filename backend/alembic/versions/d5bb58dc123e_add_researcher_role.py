"""add researcher role

Revision ID: d5bb58dc123e
Revises: c1d5012eb1cd
Create Date: 2026-08-07 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'd5bb58dc123e'
down_revision: Union[str, Sequence[str], None] = 'c1d5012eb1cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'researcher'")


def downgrade() -> None:
    pass
"""fix researcher role case

Revision ID: 72303e1de22b
Revises: d5bb58dc123e
Create Date: 2026-08-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = '72303e1de22b'
down_revision: Union[str, Sequence[str], None] = 'd5bb58dc123e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'RESEARCHER'")


def downgrade() -> None:
    pass
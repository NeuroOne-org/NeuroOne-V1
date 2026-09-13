"""add user token version

Revision ID: e3a91c5d7f20
Revises: 7544ad0b1ed6
Create Date: 2026-09-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e3a91c5d7f20"
down_revision: Union[str, Sequence[str], None] = "7544ad0b1ed6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add users.token_version, the access token's revocation counter.

    Existing rows start at 0. Tokens issued before this migration carry no
    "ver" claim at all, so they are refused and their holders sign in again.
    """

    op.add_column(
        "users",
        sa.Column(
            "token_version",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade() -> None:
    """Drop the token version column."""

    op.drop_column("users", "token_version")

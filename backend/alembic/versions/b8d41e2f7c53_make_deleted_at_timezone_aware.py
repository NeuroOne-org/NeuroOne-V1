"""make deleted_at timezone-aware on users, patients and patient_phones

Revision ID: b8d41e2f7c53
Revises: a3c7be51d904
Create Date: 2026-09-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b8d41e2f7c53"
down_revision: Union[str, Sequence[str], None] = "a3c7be51d904"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# users and patients were created naive in f1f7379b0c32; patient_phones was
# rebuilt naive in 1f74d19af1b8. visits and symptoms (a3c7be51d904) were
# created correctly and are not touched here.
TABLES = ("users", "patients", "patient_phones")


def upgrade() -> None:
    """Widen deleted_at from timestamp to timestamptz.

    No USING clause, deliberately.

    It is tempting to write ``USING deleted_at AT TIME ZONE 'UTC'`` on the
    theory that BaseModel.soft_delete() writes datetime.now(timezone.utc) and
    Postgres strips the offset, leaving naive UTC. That is not what happens.
    Assigning a timestamptz to a timestamp column *converts to the session
    TimeZone first*, then drops the zone -- so on a server set to, say,
    Asia/Colombo, an instant of 09:00Z is stored as the naive value 14:30.
    The rows hold naive LOCAL time, not naive UTC.

    Pinning the conversion to UTC would therefore reinterpret 14:30 local as
    14:30Z and shift every timestamp by the server's offset. The default
    assignment cast interprets the naive value in the session TimeZone, which
    is the exact inverse of the write path -- so it recovers the original
    instant, and does so correctly on any deployment regardless of that
    server's TimeZone setting. Verified empirically on PostgreSQL 17 with
    TimeZone=Asia/Colombo: implicit cast round-trips 09:00Z, the UTC-pinned
    variant returns 14:30Z.

    This assumes a server whose TimeZone has not changed between when rows
    were written and when this migration runs. Rows written under a different
    setting cannot be distinguished after the fact, since the stored value
    carries no record of the offset used -- that ambiguity is the bug being
    fixed here, and is why the new tables were created timezone-aware.
    """

    for table in TABLES:
        op.alter_column(
            table,
            "deleted_at",
            existing_type=sa.DateTime(),
            type_=sa.DateTime(timezone=True),
            existing_nullable=True,
        )


def downgrade() -> None:
    """Narrow deleted_at back to a naive timestamp.

    Symmetric with upgrade(): the default cast converts to the session
    TimeZone and drops the zone, reproducing exactly the values that were
    stored before the upgrade.
    """

    for table in TABLES:
        op.alter_column(
            table,
            "deleted_at",
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(),
            existing_nullable=True,
        )

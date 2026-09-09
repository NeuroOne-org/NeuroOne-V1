"""replace legacy user roles with ADMIN and CLINICIAN

Revision ID: 8e72c1f4a9b0
Revises: 72303e1de22b
Create Date: 2026-09-09
"""

from typing import Sequence, Union

from alembic import op


revision: str = "8e72c1f4a9b0"
down_revision: Union[str, Sequence[str], None] = "72303e1de22b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename DOCTOR and remove the deferred RECEPTIONIST role safely."""

    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM users
                WHERE role::text NOT IN ('DOCTOR', 'ADMIN')
            ) THEN
                RAISE EXCEPTION
                    'Cannot remove non-MVP roles while users still use them';
            END IF;
        END $$;
        """
    )
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TYPE userrole RENAME TO userrole_legacy")
    op.execute("CREATE TYPE userrole AS ENUM ('ADMIN', 'CLINICIAN')")
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN role TYPE userrole
        USING (
            CASE role::text
                WHEN 'DOCTOR' THEN 'CLINICIAN'
                WHEN 'ADMIN' THEN 'ADMIN'
            END
        )::userrole
        """
    )
    op.execute("DROP TYPE userrole_legacy")


def downgrade() -> None:
    """Restore the legacy role enum."""

    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TYPE userrole RENAME TO userrole_current")
    op.execute(
        "CREATE TYPE userrole AS ENUM ('DOCTOR', 'ADMIN', 'RECEPTIONIST')"
    )
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN role TYPE userrole
        USING (
            CASE role::text
                WHEN 'CLINICIAN' THEN 'DOCTOR'
                WHEN 'ADMIN' THEN 'ADMIN'
            END
        )::userrole
        """
    )
    op.execute("DROP TYPE userrole_current")

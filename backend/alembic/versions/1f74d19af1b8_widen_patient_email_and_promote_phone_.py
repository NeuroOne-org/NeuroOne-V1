"""widen patient email and promote patient_phones to BaseModel shape

Revision ID: 1f74d19af1b8
Revises: 8e72c1f4a9b0
Create Date: 2026-09-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1f74d19af1b8"
down_revision: Union[str, Sequence[str], None] = "8e72c1f4a9b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Widen patients.email to 255 chars and give patient_phones the standard
    UUID/timestamp/soft-delete shape used by every other table."""

    op.alter_column(
        "patients",
        "email",
        existing_type=sa.String(length=20),
        type_=sa.String(length=255),
        existing_nullable=False,
    )

    op.drop_table("patient_phones")
    op.create_table(
        "patient_phones",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column("patient_id", sa.UUID(), nullable=False),
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
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
            name=op.f("fk_patient_phones_patient_id_patients"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_patient_phones")),
    )


def downgrade() -> None:
    """Restore the legacy integer-keyed patient_phones and 20-char email."""

    op.drop_table("patient_phones")
    op.create_table(
        "patient_phones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column("patient_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
            name=op.f("fk_patient_phones_patient_id_patients"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_patient_phones")),
    )

    op.alter_column(
        "patients",
        "email",
        existing_type=sa.String(length=255),
        type_=sa.String(length=20),
        existing_nullable=False,
    )

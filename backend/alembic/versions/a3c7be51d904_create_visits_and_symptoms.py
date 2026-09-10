"""create visits and symptoms

Revision ID: a3c7be51d904
Revises: 1f74d19af1b8
Create Date: 2026-09-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "a3c7be51d904"
down_revision: Union[str, Sequence[str], None] = "1f74d19af1b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


visit_status = sa.Enum(
    "DRAFT",
    "SUBMITTED",
    "ANALYZED",
    "CLOSED",
    name="visitstatus",
)


def upgrade() -> None:
    """Create the clinical case (visit) and symptom tables.

    The composite (patient_id, visit_date) index serves the cross-visit history
    query in both directions -- Postgres scans btrees backwards, so a DESC
    ordering needs no separate index.
    """

    op.create_table(
        "visits",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("patient_id", sa.UUID(), nullable=False),
        sa.Column("visit_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("chief_complaint", sa.String(length=255), nullable=False),
        sa.Column("history", sa.Text(), nullable=True),
        sa.Column(
            "vitals",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("status", visit_status, nullable=False),
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
            ["patient_id"],
            ["patients.id"],
            name=op.f("fk_visits_patient_id_patients"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_visits")),
    )
    op.create_index(
        op.f("ix_visits_patient_id"),
        "visits",
        ["patient_id"],
        unique=False,
    )
    op.create_index(
        "ix_visits_patient_visit_date",
        "visits",
        ["patient_id", "visit_date"],
        unique=False,
    )

    op.create_table(
        "symptoms",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("visit_id", sa.UUID(), nullable=False),
        sa.Column("symptom_name", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.Integer(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=True),
        sa.Column("onset", sa.String(length=20), nullable=True),
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
        sa.CheckConstraint(
            "severity BETWEEN 1 AND 10",
            name=op.f("ck_symptoms_severity_range"),
        ),
        sa.ForeignKeyConstraint(
            ["visit_id"],
            ["visits.id"],
            name=op.f("fk_symptoms_visit_id_visits"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_symptoms")),
    )
    op.create_index(
        op.f("ix_symptoms_visit_id"),
        "symptoms",
        ["visit_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the symptom and visit tables, and the enum type they created."""

    op.drop_index(op.f("ix_symptoms_visit_id"), table_name="symptoms")
    op.drop_table("symptoms")

    op.drop_index("ix_visits_patient_visit_date", table_name="visits")
    op.drop_index(op.f("ix_visits_patient_id"), table_name="visits")
    op.drop_table("visits")

    # Postgres does not drop an enum type when the table using it is dropped,
    # so without this the next upgrade fails with "type already exists".
    visit_status.drop(op.get_bind(), checkfirst=True)

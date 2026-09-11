"""Clinical case / visit model definitions."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any
import uuid

from sqlalchemy import (
    JSON,
    UUID,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .patient import Patient
    from .scan import Scan
    from .symptom import Symptom


class VisitStatus(str, Enum):
    """Lifecycle of a clinical case.

    ANALYZED is written by the AI pipeline (AI-01), not through the visits API.
    """

    DRAFT = "draft"
    SUBMITTED = "submitted"
    ANALYZED = "analyzed"
    CLOSED = "closed"


"""
+----------------------+
|       VISIT          |
+----------------------+
| PK id                |
| FK patient_id        |
| visit_date           |
| chief_complaint      |
| history              |
| vitals               |
| notes                |
| status               |
| created_at           |
+----------------------+
"""


class Visit(BaseModel):
    """A clinical case / visit belonging to a patient.

    Ownership is derived from the parent patient -- a visit has no doctor_id of
    its own. See docs/decisions/ADR-002-visit-ownership-derivation.md.
    """

    __tablename__ = "visits"

    __table_args__ = (
        Index(
            "ix_visits_patient_visit_date",
            "patient_id",
            "visit_date",
        ),
    )

    # ForeignKey
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id"),
        nullable=False,
        index=True,
    )
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="visits",
    )

    # Table specific columns
    visit_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    chief_complaint: Mapped[str] = mapped_column(String(255), nullable=False)
    history: Mapped[str | None] = mapped_column(Text, nullable=True)

    # JSON rather than columns: vitals are never queried or filtered, only read
    # as a whole by the AI context builder. The shape is enforced at the API
    # boundary by the Vitals schema.
    vitals: Mapped[dict[str, Any]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
        default=dict,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[VisitStatus] = mapped_column(
        SQLEnum(VisitStatus),
        default=VisitStatus.DRAFT,
        nullable=False,
    )

    # Always load through VisitRepository._with_symptoms, which filters
    # soft-deleted rows in the eager query. A bare select(Visit) would load
    # is_deleted=True symptoms.
    symptoms: Mapped[list["Symptom"]] = relationship(
        "Symptom",
        back_populates="visit",
        cascade="all, delete-orphan",
        order_by="Symptom.created_at",
    )

    # MRI is a primary input, but optional: an analysis can still run on
    # symptoms alone (ADR-006). One scan per visit -- a follow-up scan
    # belongs to a new visit, not a replacement of this one.
    scan: Mapped["Scan | None"] = relationship(
        "Scan",
        back_populates="visit",
        uselist=False,
        cascade="all, delete-orphan",
    )

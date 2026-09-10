"""Symptom model definitions."""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import UUID, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .visit import Visit


"""
+---------------------+
|      SYMPTOM        |
+---------------------+
| PK id               |
| FK visit_id         |
| symptom_name        |
| severity            |
| duration_days       |
| onset               |
+---------------------+
"""


class Symptom(BaseModel):
    """A neurological symptom recorded against a clinical case."""

    __tablename__ = "symptoms"

    __table_args__ = (
        CheckConstraint(
            "severity BETWEEN 1 AND 10",
            name="severity_range",
        ),
    )

    # ForeignKey
    visit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("visits.id"),
        nullable=False,
        index=True,
    )
    visit: Mapped["Visit"] = relationship(
        "Visit",
        back_populates="symptoms",
    )

    # Table specific columns
    symptom_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Integer, not free text: cross-visit trend detection needs a comparable
    # magnitude ("tremor 3 -> 5 -> 8").
    severity: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    onset: Mapped[str | None] = mapped_column(String(20), nullable=True)

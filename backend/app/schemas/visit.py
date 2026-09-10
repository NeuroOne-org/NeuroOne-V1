"""Clinical case / visit request and response schemas."""

from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.visit import VisitStatus
from app.schemas.common import PaginatedResponse
from app.schemas.symptom import SymptomCreate, SymptomResponse


def _as_utc(value: datetime | None) -> datetime | None:
    """Normalize a naive datetime to UTC so ordering never mixes tz-awareness."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


class Vitals(BaseModel):
    """Vital signs recorded at a visit.

    Persisted as JSON, so this schema is the only thing enforcing the shape the
    AI context builder reads.
    """

    model_config = ConfigDict(extra="forbid")

    bp_systolic: int | None = Field(default=None, ge=0, le=300)
    bp_diastolic: int | None = Field(default=None, ge=0, le=200)
    heart_rate: int | None = Field(default=None, ge=0, le=300)
    respiratory_rate: int | None = Field(default=None, ge=0, le=100)
    temperature_c: float | None = Field(default=None, ge=25, le=45)
    spo2: int | None = Field(default=None, ge=0, le=100)
    weight_kg: float | None = Field(default=None, ge=0, le=700)
    height_cm: float | None = Field(default=None, ge=0, le=300)


class VisitBase(BaseModel):
    """Fields shared by visit request and response schemas."""

    chief_complaint: str = Field(min_length=1, max_length=255)
    history: str | None = None
    vitals: Vitals = Field(default_factory=Vitals)
    notes: str | None = None


class VisitCreate(VisitBase):
    """Payload used to open a clinical case.

    Symptoms may be supplied inline so the case saves in one request, mirroring
    APP-FLOW section 4.
    """

    visit_date: datetime | None = None
    status: VisitStatus | None = None
    symptoms: list[SymptomCreate] = Field(default_factory=list)

    @field_validator("visit_date")
    @classmethod
    def _normalize_visit_date(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value)


class VisitUpdate(BaseModel):
    """Payload used to partially update a visit.

    Deliberately has no ``symptoms`` field: symptom ids are referenced by the
    AI trend_basis, so a wholesale replace would invalidate them. Symptoms are
    mutated through the symptom endpoints instead.
    """

    chief_complaint: str | None = Field(default=None, min_length=1, max_length=255)
    history: str | None = None
    vitals: Vitals | None = None
    notes: str | None = None
    visit_date: datetime | None = None
    status: VisitStatus | None = None

    @field_validator("visit_date")
    @classmethod
    def _normalize_visit_date(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value)


class VisitResponse(VisitBase):
    """Public visit data returned by the API.

    Exposes ``patient_id`` only -- no nested patient or doctor object, so no
    endpoint can lazy-load a relationship per row.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    patient_id: UUID
    visit_date: datetime
    status: VisitStatus
    symptoms: list[SymptomResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class VisitListResponse(PaginatedResponse[VisitResponse]):
    """Paginated visit collection returned by list endpoints."""


class VisitHistoryResponse(BaseModel):
    """A patient's visit history, ordered for cross-visit trend comparison.

    Not a paginated envelope on purpose: history is a bounded window, and
    page/total_pages are meaningless alongside exclude_visit_id.
    """

    patient_id: UUID
    total_visits: int = Field(ge=0)
    returned: int = Field(ge=0)
    order: Literal["asc", "desc"]
    visits: list[VisitResponse]


__all__ = [
    "VisitBase",
    "VisitCreate",
    "VisitHistoryResponse",
    "VisitListResponse",
    "VisitResponse",
    "VisitUpdate",
    "Vitals",
]

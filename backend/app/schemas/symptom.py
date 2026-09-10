"""Symptom request and response schemas."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.common import PaginatedResponse


# Kept as a Literal rather than a DB enum: this vocabulary is clinician-facing
# and expected to churn, and ALTER TYPE ... ADD VALUE migrations are a tax.
SymptomOnset = Literal["sudden", "subacute", "gradual", "insidious", "unknown"]

# FR-03 requires observations as a structured field, distinct from severity,
# duration, and onset -- not collapsed into a free-text blob (AGENTS.md
# section 7). Bounded so a clinician's note stays a note, not a document.
OBSERVATION_MAX_LENGTH = 2000


def _reject_blank(value: str | None) -> str | None:
    """A whitespace-only observation is the same as no observation, rejected
    rather than silently accepted as content."""
    if value is not None and not value.strip():
        raise ValueError("observation must not be blank")
    return value


class SymptomBase(BaseModel):
    """Fields shared by symptom request and response schemas."""

    symptom_name: str = Field(min_length=1, max_length=100)
    severity: int = Field(ge=1, le=10)
    duration_days: int | None = Field(default=None, ge=0)
    onset: SymptomOnset | None = None
    observation: str | None = Field(default=None, max_length=OBSERVATION_MAX_LENGTH)

    @field_validator("observation")
    @classmethod
    def _validate_observation(cls, value: str | None) -> str | None:
        return _reject_blank(value)


class SymptomCreate(SymptomBase):
    """Payload used to record a symptom against a visit."""


class SymptomUpdate(BaseModel):
    """Payload used to partially update a symptom."""

    symptom_name: str | None = Field(default=None, min_length=1, max_length=100)
    severity: int | None = Field(default=None, ge=1, le=10)
    duration_days: int | None = Field(default=None, ge=0)
    onset: SymptomOnset | None = None
    observation: str | None = Field(default=None, max_length=OBSERVATION_MAX_LENGTH)

    @field_validator("observation")
    @classmethod
    def _validate_observation(cls, value: str | None) -> str | None:
        return _reject_blank(value)


class SymptomResponse(SymptomBase):
    """Public symptom data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    visit_id: UUID
    created_at: datetime
    updated_at: datetime


class SymptomListResponse(PaginatedResponse[SymptomResponse]):
    """Paginated symptom collection returned by list endpoints."""


__all__ = [
    "SymptomBase",
    "SymptomCreate",
    "SymptomListResponse",
    "SymptomOnset",
    "SymptomResponse",
    "SymptomUpdate",
]

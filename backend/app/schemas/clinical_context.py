"""Normalized clinical context supplied to the AI pipeline.

This is the "Build Clinical Context" stage of the pipeline (TRD section 8) in
schema form. It is deliberately PHI-minimal: per AGENTS.md section 12 it carries
no name, email, phone, address, or date of birth. Age is reduced to whole years
and sex to the single stored character, because that is all the reasoning layer
needs.
"""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.symptom import SymptomOnset


TrendDirection = Literal["worsening", "improving", "fluctuating", "stable"]


class ContextSymptom(BaseModel):
    """A symptom as the AI layer sees it."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    symptom_name: str = Field(min_length=1)
    severity: int = Field(ge=1, le=10)
    duration_days: int | None = Field(default=None, ge=0)
    onset: SymptomOnset | None = None
    observation: str | None = None


class ContextVisit(BaseModel):
    """A clinical case as the AI layer sees it."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    visit_date: datetime
    chief_complaint: str
    history: str | None = None
    vitals: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None
    symptoms: list[ContextSymptom] = Field(default_factory=list)


class TrendPoint(BaseModel):
    """One observation of a symptom at one visit.

    Carries the real visits.id and symptoms.id so a trend stays traceable back
    to the rows it was derived from.
    """

    visit_id: UUID
    symptom_id: UUID
    visit_date: datetime
    severity: int = Field(ge=1, le=10)


class SymptomTrend(BaseModel):
    """How one symptom moved across a patient's visits.

    Only symptoms observed at two or more distinct visits produce a trend --
    a single observation is a snapshot, not a direction.
    """

    symptom_name: str = Field(min_length=1)
    direction: TrendDirection
    first_severity: int = Field(ge=1, le=10)
    latest_severity: int = Field(ge=1, le=10)
    visit_span: int = Field(ge=2)
    points: list[TrendPoint] = Field(min_length=2)


class ClinicalContext(BaseModel):
    """Everything the AI pipeline is allowed to reason over.

    ``prior_visits`` is ordered oldest-first, which is the order trend
    detection wants and the order CASE-01's history retrieval already provides.
    """

    model_config = ConfigDict(extra="forbid")

    patient_id: UUID
    visit_id: UUID
    current_visit: ContextVisit
    prior_visits: list[ContextVisit] = Field(default_factory=list)
    trends: list[SymptomTrend] = Field(default_factory=list)
    patient_age_years: int | None = Field(default=None, ge=0, le=130)
    patient_sex: str | None = Field(default=None, max_length=1)

    @property
    def all_visits(self) -> list[ContextVisit]:
        """Every visit oldest-first, with the current visit last."""

        return [*self.prior_visits, self.current_visit]


__all__ = [
    "ClinicalContext",
    "ContextSymptom",
    "ContextVisit",
    "SymptomTrend",
    "TrendDirection",
    "TrendPoint",
]

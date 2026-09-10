"""Clinical report contract (FR-07, ADR-004).

``ReportSnapshot`` is exactly what ``backend/app/reports/renderer.py`` may
see -- it is built once, at generation time, from the resolved analysis,
visit, and patient, and then persisted whole. A download re-renders from the
stored snapshot; it never re-reads the (possibly since-edited) source rows.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.analysis import DiagnosisCategory, LikelihoodBand
from app.schemas.common import PaginatedResponse


class ReportPatientSnapshot(BaseModel):
    """The patient/case identification FR-07 requires a report to carry."""

    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(min_length=1)
    age_years: int | None = Field(default=None, ge=0, le=130)
    gender: str | None = None


class ReportSymptomSnapshot(BaseModel):
    """One clinical input as recorded for the visit (FR-03)."""

    model_config = ConfigDict(extra="forbid")

    symptom_name: str
    severity: int = Field(ge=1, le=10)
    duration_days: int | None = None
    onset: str | None = None
    observation: str | None = None


class ReportVisitSnapshot(BaseModel):
    """The clinical case the analysis was run against."""

    model_config = ConfigDict(extra="forbid")

    visit_date: datetime
    chief_complaint: str
    history: str | None = None
    notes: str | None = None
    symptoms: list[ReportSymptomSnapshot] = Field(default_factory=list)


class ReportEvidenceSnapshot(BaseModel):
    """A citation as it must appear in the PDF (FR-05/06)."""

    model_config = ConfigDict(extra="forbid")

    source: str
    citation: str
    relevant_passage: str
    source_url: str | None = None
    source_tier: str | None = None
    published_year: int | None = None


class ReportFindingSnapshot(BaseModel):
    """One ranked candidate, expressed as the safety boundary requires:

    likelihood, never certainty; category, never a definitive diagnosis.
    """

    model_config = ConfigDict(extra="forbid")

    rank: int
    condition_name: str
    category: DiagnosisCategory
    likelihood_band: LikelihoodBand
    supporting_findings: list[str]
    contradicting_findings: list[str] = Field(default_factory=list)
    explanation: str
    trend_basis: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[ReportEvidenceSnapshot] = Field(min_length=1)


class ReportSnapshot(BaseModel):
    """Everything the renderer may draw on. Nothing else reaches the PDF."""

    model_config = ConfigDict(extra="forbid")

    analysis_id: UUID
    visit_id: UUID
    patient: ReportPatientSnapshot
    visit: ReportVisitSnapshot
    model_name: str
    provider_mode: str
    pipeline_note: str
    disclaimer: str
    generated_at: datetime
    findings: list[ReportFindingSnapshot] = Field(min_length=1)


# --------------------------------------------------------------------------
# Wire schemas
# --------------------------------------------------------------------------


class ReportResponse(BaseModel):
    """A generated report's metadata, as returned by the API.

    Deliberately excludes ``snapshot``: it is the renderer's input, not a
    public field, and can be sizeable (mirrors ``Analysis.context_snapshot``
    staying off ``AnalysisResponse``).
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    analysis_id: UUID
    generated_by_id: UUID
    generated_at: datetime
    filename: str
    created_at: datetime
    updated_at: datetime


class ReportListResponse(PaginatedResponse[ReportResponse]):
    """Paginated report collection returned by list endpoints."""


__all__ = [
    "ReportEvidenceSnapshot",
    "ReportFindingSnapshot",
    "ReportListResponse",
    "ReportPatientSnapshot",
    "ReportResponse",
    "ReportSnapshot",
    "ReportSymptomSnapshot",
    "ReportVisitSnapshot",
]

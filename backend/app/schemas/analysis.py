"""Structured differential-diagnosis contract (AGENTS.md section 8.2).

Decision support, never a definitive diagnosis. Section 8.2 is explicit that the
prohibition reaches field naming, not just prose: there is deliberately no
``final_diagnosis``, no ``doctor_verified``, no ``certainty``, no ``probability``
and no bare ``diagnosis`` field anywhere in this module.
"""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    model_validator,
)

from app.schemas.clinical_context import ClinicalContext
from app.schemas.common import PaginatedResponse
from app.schemas.evidence import EvidenceRef, RetrievedDocument


DiagnosisCategory = Literal["differential_diagnosis", "early_watch"]
ProviderMode = Literal["simulated", "live"]
LikelihoodBand = Literal["low", "moderate", "high"]

# Section 8.2 forbids expressing certainty, so the pipeline clamps below 1.0.
MAX_CONFIDENCE = 0.92
MODERATE_CONFIDENCE = 0.40
HIGH_CONFIDENCE = 0.70

# Section 8.1: mock-sourced output must stay labeled as simulated.
SIMULATED_PIPELINE_NOTE = "pipeline complete, evidence retrieval simulated"

DISCLAIMER = (
    "Decision support only. This is a ranked set of possible conditions with "
    "supporting evidence, not a diagnosis. The clinician remains responsible "
    "for final interpretation."
)


def likelihood_band_for(confidence: float) -> LikelihoodBand:
    """Tier a confidence value (AGENTS.md section 8.3).

    Derived, never stored: a persisted copy could drift from the number it is
    supposed to describe (ADR-003).
    """
    if confidence >= HIGH_CONFIDENCE:
        return "high"
    if confidence >= MODERATE_CONFIDENCE:
        return "moderate"
    return "low"


class TrendBasisRef(BaseModel):
    """A pointer into the patient's OWN visit history.

    Distinct from ``EvidenceRef``, which points at external literature
    (AGENTS.md section 8.2). The ids are real ``visits.id`` / ``symptoms.id``
    values, but they are soft references by design (ADR-003): an analysis is a
    snapshot of reasoning, so a later edit to the underlying record must not
    rewrite what a past analysis said.
    """

    model_config = ConfigDict(extra="forbid")

    visit_id: UUID
    symptom_id: UUID | None = None
    symptom_name: str = Field(min_length=1)
    visit_date: datetime
    severity: int | None = Field(default=None, ge=1, le=10)
    observation: str = Field(min_length=1)


class DiagnosisCandidate(BaseModel):
    """One ranked possible condition.

    ``extra="forbid"`` is deliberate: a model that invents a field is a contract
    failure, not a field to ignore.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    category: DiagnosisCategory
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_findings: list[str] = Field(min_length=1)
    contradicting_findings: list[str] = Field(default_factory=list)
    explanation: str = Field(min_length=1)
    trend_basis: list[TrendBasisRef] = Field(default_factory=list)

    # Every ranked condition carries at least one citation. An uncited
    # recommendation is exactly the untraceable output AGENTS.md section 18
    # forbids, so this is enforced at the type level rather than by convention.
    #
    # Typed as the full RetrievedDocument, not the 3-field EvidenceRef: a
    # provider names evidence by document_id, but the orchestrator resolves
    # that id back against its own retrieved set and overwrites the content
    # (AGENTS.md section 8.4.4 -- source metadata must be preserved end to
    # end, not narrowed away at the point a candidate is built).
    evidence: list[RetrievedDocument] = Field(min_length=1)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def likelihood_band(self) -> LikelihoodBand:
        """Confidence-tiered output (section 8.3).

        This is what UI copy and the PDF should render, rather than the raw
        number, so that likelihood never reads as a precise claim.
        """
        return likelihood_band_for(self.confidence)

    @model_validator(mode="after")
    def _early_watch_requires_trend_basis(self) -> "DiagnosisCandidate":
        """An early-watch flag must point at the patient's own history.

        Note the implication runs one way only: a differential_diagnosis MAY
        also carry trend_basis. trend_basis is a trace, not a category marker.
        """
        if self.category == "early_watch" and not self.trend_basis:
            raise ValueError(
                "category 'early_watch' requires at least one trend_basis "
                "reference (AGENTS.md 8.2): an early-watch flag must be "
                "traceable to the patient's own visit history."
            )
        return self


class ReasoningRequest(BaseModel):
    """What the orchestrator hands the LLM provider."""

    model_config = ConfigDict(extra="forbid")

    context: ClinicalContext
    evidence: list[RetrievedDocument] = Field(default_factory=list)
    max_candidates: int = Field(default=5, ge=1, le=10)


class ReasoningResult(BaseModel):
    """What the LLM provider returns.

    Validated at the seam, so a real provider in AI-02 that returns malformed
    output fails here and becomes a controlled AIError.
    """

    model_config = ConfigDict(extra="forbid")

    model_name: str = Field(min_length=1, max_length=100)
    provider_mode: ProviderMode

    # An empty list is permitted here but not on AnalysisResult: a provider
    # reporting "nothing matched" is a legitimate answer, distinct from a
    # provider returning malformed output. The orchestrator decides what an
    # empty differential means and raises a distinct error code for it.
    candidates: list[DiagnosisCandidate] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """Validated pipeline output, before persistence."""

    model_config = ConfigDict(extra="forbid")

    visit_id: UUID
    patient_id: UUID
    model_name: str = Field(min_length=1, max_length=100)
    provider_mode: ProviderMode
    pipeline_note: str = Field(min_length=1)
    disclaimer: str = Field(min_length=1)
    generated_at: datetime
    candidates: list[DiagnosisCandidate] = Field(min_length=1)

    @model_validator(mode="after")
    def _candidates_ranked_descending(self) -> "AnalysisResult":
        confidences = [candidate.confidence for candidate in self.candidates]
        if any(
            earlier < later
            for earlier, later in zip(confidences, confidences[1:])
        ):
            raise ValueError(
                "candidates must be ranked by descending confidence."
            )
        return self


# --------------------------------------------------------------------------
# Wire schemas
# --------------------------------------------------------------------------


class AnalysisCreateRequest(BaseModel):
    """Options for triggering an analysis.

    Every field has a default so the demo journey can POST an empty body.
    """

    model_config = ConfigDict(extra="forbid")

    history_limit: int = Field(default=10, ge=0, le=50)


class EvidenceResponse(EvidenceRef):
    """A citation as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    document_id: str | None = None
    chunk_id: str | None = None
    source_url: str | None = None
    source_tier: str | None = None
    published_year: int | None = None
    relevance_score: float | None = None


class FindingResponse(BaseModel):
    """A ranked candidate as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    rank: int
    name: str = Field(validation_alias="condition_name")
    category: DiagnosisCategory
    confidence: float
    supporting_findings: list[str]
    contradicting_findings: list[str]
    explanation: str
    trend_basis: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[EvidenceResponse] = Field(default_factory=list)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def likelihood_band(self) -> LikelihoodBand:
        """Derived from confidence, never read from the row."""
        return likelihood_band_for(self.confidence)


class AnalysisResponse(BaseModel):
    """A persisted analysis as returned by the API.

    ``provider_mode`` and ``pipeline_note`` are surfaced on the wire, not merely
    kept internally: a consumer must be able to tell simulated evidence from
    live evidence without reading the source.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    visit_id: UUID
    model_name: str
    provider_mode: str
    pipeline_note: str
    disclaimer: str
    generated_at: datetime
    findings: list[FindingResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class AnalysisListResponse(PaginatedResponse[AnalysisResponse]):
    """Paginated analysis collection returned by list endpoints."""


__all__ = [
    "AnalysisCreateRequest",
    "AnalysisListResponse",
    "AnalysisResponse",
    "AnalysisResult",
    "DISCLAIMER",
    "DiagnosisCandidate",
    "DiagnosisCategory",
    "EvidenceResponse",
    "FindingResponse",
    "HIGH_CONFIDENCE",
    "LikelihoodBand",
    "likelihood_band_for",
    "MAX_CONFIDENCE",
    "MODERATE_CONFIDENCE",
    "ProviderMode",
    "ReasoningRequest",
    "ReasoningResult",
    "SIMULATED_PIPELINE_NOTE",
    "TrendBasisRef",
]

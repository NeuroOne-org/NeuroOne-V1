"""Imaging staging contract (ADR-006).

A third provider seam alongside the retriever and the reasoning client
(ADR-003, ADR-005): schema-real, provider-mocked, deterministic, labelled as
simulated. The stage estimate produced here becomes one ranked candidate
inside the same DiagnosisCandidate/AnalysisFinding shape (ADR-006 decision 3)
-- it never gets its own field on the wire, because it must never read as a
lone verdict.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


StageLabel = Literal["CN", "MCI", "Mild", "Moderate", "Severe"]

# Mirrors app.schemas.analysis.ProviderMode. Duplicated rather than imported:
# schemas must not depend on each other's unrelated constants, and
# app.schemas.analysis importing StagingResult (below) the other way would
# otherwise cycle back here.
ImagingProviderMode = Literal["simulated", "live"]

# The human-readable condition name each code expands to. Shared between the
# orchestrator (which needs it to query literature about the stage) and the
# mock corpus (whose staging conditions are keyed by the same text), so the
# two sides cannot drift apart.
STAGE_LABELS: dict[StageLabel, str] = {
    "CN": "Cognitively normal",
    "MCI": "Mild cognitive impairment (MCI)",
    "Mild": "Mild dementia",
    "Moderate": "Moderate dementia",
    "Severe": "Severe dementia",
}

# Ordinal scale for cross-visit stage-trend detection (ADR-006 consequence:
# "detect_trends must be extended ... unless scan-derived metrics feed it,
# the trend story stays symptom-only"). A rank, not a score -- it exists so
# app.ai.trends can classify a direction across visits, never to be surfaced
# as a number on the wire.
STAGE_ORDER: dict[StageLabel, int] = {
    "CN": 0,
    "MCI": 1,
    "Mild": 2,
    "Moderate": 3,
    "Severe": 4,
}


class RegionContribution(BaseModel):
    """One anatomical region's weight in a staging estimate.

    Descriptive detail only. Region attribution as its own feature is a hard
    exclusion (ADR-006 "Risks"); this is the staging provider's supporting
    detail for a stage it already produced, not a segmentation measurement.
    """

    model_config = ConfigDict(extra="forbid")

    region: str = Field(min_length=1, max_length=100)
    contribution: float = Field(ge=0.0, le=1.0)


class StagingRequest(BaseModel):
    """What the orchestrator hands the imaging staging provider.

    Deliberately narrow: the scan's storage key and original filename never
    leave the database layer (AGENTS.md section 12, PHI minimization). The
    provider reasons over the scan's own metadata, nothing patient-identifying.
    """

    model_config = ConfigDict(extra="forbid")

    checksum: str = Field(min_length=1, max_length=64)
    content_type: str = Field(min_length=1, max_length=100)
    dimensions: dict[str, Any] = Field(default_factory=dict)


class StagingResult(BaseModel):
    """What the imaging staging provider returns.

    Validated at the seam, exactly like ``ReasoningResult``: a real staging
    model that returns malformed output fails here, not on a clinician's
    screen.
    """

    model_config = ConfigDict(extra="forbid")

    model_name: str = Field(min_length=1, max_length=100)
    provenance: ImagingProviderMode
    stage: StageLabel

    # Section 8.2's certainty ceiling (MAX_CONFIDENCE = 0.92) applies here
    # too. It is enforced by the provider that constructs this value, not by
    # a field constraint: importing MAX_CONFIDENCE from app.schemas.analysis
    # here would cycle back, since that module holds ReasoningRequest.imaging.
    confidence: float = Field(ge=0.0, le=1.0)

    contributing_regions: list[RegionContribution] = Field(default_factory=list)


__all__ = [
    "STAGE_LABELS",
    "STAGE_ORDER",
    "ImagingProviderMode",
    "RegionContribution",
    "StageLabel",
    "StagingRequest",
    "StagingResult",
]

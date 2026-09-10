"""Literature evidence schemas.

``EvidenceRef`` is exactly the three fields AGENTS.md section 8.2 specifies for
``evidence[]`` -- it is the wire shape. ``RetrievedDocument`` extends it with the
provider-side metadata section 8.4.4 requires be preserved. Subclassing means
``EvidenceRef.model_validate(document)`` narrows a full record to the wire shape
without a hand-written mapping.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SourceTier = Literal[
    "guideline",
    "systematic_review",
    "primary_study",
    "reference_text",
]


class EvidenceRef(BaseModel):
    """A citation attached to a ranked candidate.

    Traces to EXTERNAL literature. Not to be confused with ``TrendBasisRef``,
    which traces to the patient's own visit history (AGENTS.md section 8.2:
    "Do not conflate them").
    """

    model_config = ConfigDict(from_attributes=True)

    source: str = Field(min_length=1, max_length=255)
    citation: str = Field(min_length=1, max_length=500)
    relevant_passage: str = Field(min_length=1)


class RetrievedDocument(EvidenceRef):
    """A corpus record as the retriever returns it.

    The extra fields are source metadata (section 8.4.4). They are persisted but
    not all surfaced on the wire.
    """

    document_id: str = Field(min_length=1, max_length=100)
    chunk_id: str = Field(min_length=1, max_length=100)
    source_url: str | None = Field(default=None, max_length=500)
    source_tier: SourceTier
    published_year: int | None = Field(default=None, ge=1800, le=2200)
    keywords: tuple[str, ...] = ()
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0)


class RetrievalQuery(BaseModel):
    """What the orchestrator asks the retriever for."""

    model_config = ConfigDict(extra="forbid")

    condition_names: list[str] = Field(default_factory=list)
    symptom_names: list[str] = Field(default_factory=list)
    chief_complaint: str = ""

    # Retrieval happens once, before reasoning (TRD section 8), so the cap has
    # to cover every candidate's citations rather than a single condition's.
    max_results: int = Field(default=12, ge=1, le=50)


__all__ = [
    "EvidenceRef",
    "RetrievalQuery",
    "RetrievedDocument",
    "SourceTier",
]

"""The provider seam.

This module is the entire surface AI-02 replaces. Everything else in the
pipeline -- context building, trend detection, ranking, citation attachment,
validation, persistence -- is real now and stays unchanged when a live corpus
and a live model arrive (AGENTS.md section 8.1, ADR-003).

Two narrow protocols rather than one combined provider, because retrieval and
reasoning fail differently and are swapped independently.
"""

from typing import Literal, Protocol, runtime_checkable

from app.schemas.analysis import ReasoningRequest, ReasoningResult
from app.schemas.evidence import RetrievalQuery, RetrievedDocument
from app.schemas.imaging import StagingRequest, StagingResult


ProviderMode = Literal["simulated", "live"]


@runtime_checkable
class EvidenceRetriever(Protocol):
    """Retrieves candidate literature for a clinical context.

    Implementations must preserve source metadata (AGENTS.md section 8.4.4):
    the returned documents carry the citation, the passage, and the provenance
    that make a recommendation traceable.
    """

    name: str
    provenance: ProviderMode

    def retrieve(self, query: RetrievalQuery) -> list[RetrievedDocument]:
        """Return documents relevant to the query, most relevant first.

        Returning an empty list is a legitimate outcome, not an error -- the
        orchestrator decides what an absence of evidence means.
        """
        ...


@runtime_checkable
class LLMClient(Protocol):
    """Produces ranked candidate conditions from context plus evidence.

    The return type is the same ``DiagnosisCandidate`` model the API serves, so
    a live model that returns malformed output fails validation here, at the
    seam, and becomes a controlled AIError rather than reaching the database.
    """

    name: str
    provenance: ProviderMode

    def generate_analysis(self, request: ReasoningRequest) -> ReasoningResult:
        """Reason over the supplied context and evidence."""
        ...


@runtime_checkable
class ImagingStager(Protocol):
    """Produces a dementia-stage estimate from one MRI scan's metadata.

    The third seam ADR-006 adds alongside retrieval and reasoning. A staging
    provider never has direct clinical authority -- its output becomes one
    candidate inside the same cited, ranked differential everything else in
    the pipeline already produces (ADR-006 decision 3), not a field of its
    own on the wire.
    """

    name: str
    provenance: ProviderMode

    def stage(self, request: StagingRequest) -> StagingResult:
        """Return a stage estimate for the supplied scan metadata."""
        ...


__all__ = ["EvidenceRetriever", "ImagingStager", "LLMClient", "ProviderMode"]

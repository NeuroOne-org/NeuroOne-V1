"""Rank Evidence (TRD section 8, stage 4).

Real now and unchanged by AI-02: ranking operates on whatever the retriever
returned, so a live corpus is ordered by the same rules as the mock one
(AGENTS.md section 8.1).
"""

from collections.abc import Sequence

from app.schemas.analysis import DiagnosisCandidate
from app.schemas.evidence import RetrievedDocument


# AGENTS.md section 8.4: trusted medical sources are prioritized. Applied here
# rather than inside a provider, so it holds for every provider.
TIER_PRIORITY = {
    "guideline": 0,
    "systematic_review": 1,
    "primary_study": 2,
    "reference_text": 3,
}


def rank_evidence(
    documents: Sequence[RetrievedDocument],
    *,
    limit: int | None = None,
) -> list[RetrievedDocument]:
    """Order documents by relevance, then source trust, then recency.

    ``document_id`` is the final tie-break so the ordering is total and two
    identical runs produce identical output.
    """

    ordered = sorted(
        documents,
        key=lambda document: (
            -document.relevance_score,
            TIER_PRIORITY.get(document.source_tier, len(TIER_PRIORITY)),
            -(document.published_year or 0),
            document.document_id,
        ),
    )

    return ordered[:limit] if limit is not None else ordered


def rank_candidates(
    candidates: Sequence[DiagnosisCandidate],
    *,
    limit: int | None = None,
) -> list[DiagnosisCandidate]:
    """Order candidates by descending confidence, name breaking ties."""

    ordered = sorted(
        candidates,
        key=lambda candidate: (-candidate.confidence, candidate.name),
    )

    return ordered[:limit] if limit is not None else ordered


def cap_evidence_per_candidate(
    candidates: Sequence[DiagnosisCandidate],
    *,
    limit: int,
) -> list[DiagnosisCandidate]:
    """Trim each candidate's citations to the configured maximum.

    Trimming never empties the list: a candidate that reached this point has at
    least one citation, and ``limit`` is validated to be positive.
    """

    if limit < 1:
        raise ValueError("evidence limit must be at least 1")

    return [
        candidate.model_copy(update={"evidence": candidate.evidence[:limit]})
        for candidate in candidates
    ]


__all__ = [
    "TIER_PRIORITY",
    "cap_evidence_per_candidate",
    "rank_candidates",
    "rank_evidence",
]

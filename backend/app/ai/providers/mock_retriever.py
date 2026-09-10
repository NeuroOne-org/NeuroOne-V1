"""Deterministic stand-in for a literature retriever.

Matches the query against a frozen corpus by keyword overlap. Returns documents
most-relevant-first, with a stable tie-break so repeated runs are identical.

SIMULATED: the corpus is a fixture, not real literature. AI-02 replaces this
class behind ``EvidenceRetriever``.
"""

from app.ai.corpus.mock_corpus import MOCK_DOCUMENTS
from app.schemas.evidence import RetrievalQuery, RetrievedDocument


# Weight per matched term, by where the match came from.
CONDITION_MATCH = 0.5
SYMPTOM_MATCH = 0.3
COMPLAINT_MATCH = 0.2

# Guideline and systematic review outrank primary studies and reference text,
# so "trusted medical sources are prioritized" (AGENTS.md section 8.4).
TIER_BONUS = {
    "guideline": 0.10,
    "systematic_review": 0.08,
    "primary_study": 0.04,
    "reference_text": 0.0,
}


def _normalize(value: str) -> str:
    return " ".join(value.split()).casefold()


class MockEvidenceRetriever:
    """Keyword retriever over the frozen mock corpus."""

    name = "mock-corpus-v1"
    provenance = "simulated"

    def __init__(self, documents: tuple[RetrievedDocument, ...] = MOCK_DOCUMENTS):
        self._documents = documents

    def _score(self, document: RetrievedDocument, query: RetrievalQuery) -> float:
        keywords = {_normalize(keyword) for keyword in document.keywords}
        if not keywords:
            return 0.0

        conditions = {_normalize(name) for name in query.condition_names}
        symptoms = {_normalize(name) for name in query.symptom_names}
        complaint = _normalize(query.chief_complaint)

        score = 0.0
        score += CONDITION_MATCH * len(keywords & conditions)
        score += SYMPTOM_MATCH * len(keywords & symptoms)

        if complaint:
            score += COMPLAINT_MATCH * sum(
                1 for keyword in keywords if keyword in complaint
            )

        if score == 0.0:
            return 0.0

        return score + TIER_BONUS.get(document.source_tier, 0.0)

    def retrieve(self, query: RetrievalQuery) -> list[RetrievedDocument]:
        """Return matching documents, most relevant first.

        An empty result is a legitimate outcome -- deciding what missing
        evidence means belongs to the orchestrator, not here.
        """

        scored: list[tuple[float, RetrievedDocument]] = []
        for document in self._documents:
            score = self._score(document, query)
            if score > 0.0:
                scored.append((score, document))

        if not scored:
            return []

        highest = max(score for score, _ in scored)

        # Sort by score, then document_id: a total order, so repeated runs
        # return byte-identical results.
        scored.sort(key=lambda pair: (-pair[0], pair[1].document_id))

        return [
            document.model_copy(
                update={"relevance_score": round(min(score / highest, 1.0), 4)}
            )
            for score, document in scored[: query.max_results]
        ]


__all__ = ["MockEvidenceRetriever"]

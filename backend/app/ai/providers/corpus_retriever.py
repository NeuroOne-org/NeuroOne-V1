"""Live retriever over the curated corpus (ADR-007, AI-02b-5).

Database-free, like every provider in `app/ai/` (ADR-003 section 2): every
query against Postgres lives in `CorpusRepository`
(`app/repositories/corpus_repository.py`), reached only through the
`CorpusSearch` protocol this module depends on
(`app/ai/providers/base.py`).
"""

import logging

from app.ai.corpus.policy import ALLOWED_TIERS
from app.ai.providers.base import CorpusHit, CorpusSearch, CorpusSearchTerms
from app.ai.ranking import TIER_BONUS
from app.schemas.evidence import RetrievalQuery, RetrievedDocument


logger = logging.getLogger(__name__)

# Clinician free text is unbounded; a term cap keeps the query shape
# predictable regardless of how long a chief complaint is (ADR-007 decision
# 6, mirrored by the repository's own SQL term-shaping).
MAX_COMPLAINT_TOKENS = 20


def _build_terms(query: RetrievalQuery) -> CorpusSearchTerms:
    return CorpusSearchTerms(
        conditions=tuple(query.condition_names),
        symptoms=tuple(query.symptom_names),
        complaint_terms=tuple(query.chief_complaint.split()[:MAX_COMPLAINT_TOKENS]),
    )


def _to_retrieved_document(hit: CorpusHit, score: float) -> RetrievedDocument:
    return RetrievedDocument(
        source=hit.source,
        citation=hit.citation,
        relevant_passage=hit.relevant_passage,
        document_id=hit.document_id,
        chunk_id=hit.chunk_id,
        source_url=hit.source_url,
        source_tier=hit.source_tier,
        published_year=hit.published_year,
        keywords=hit.keywords,
        relevance_score=score,
    )


class CorpusEvidenceRetriever:
    """`EvidenceRetriever` backed by the curated corpus (ADR-007 decision 5).

    Owns query shaping, tier re-filtering, score normalization and
    determinism; `CorpusSearch` owns nothing but the search itself.
    """

    provenance = "live"

    def __init__(self, search: CorpusSearch, *, corpus_version: str):
        self._search = search
        self.corpus_version = corpus_version
        self.name = f"curated-corpus-{corpus_version}"

    def retrieve(self, query: RetrievalQuery) -> list[RetrievedDocument]:
        """Return matching, active corpus rows, most relevant first.

        An empty result is a legitimate outcome -- deciding what missing
        evidence means belongs to the orchestrator, not here. A search
        failure is not caught here either: it propagates to the
        orchestrator, which maps it to `AIError(rag_error)`.
        """

        terms = _build_terms(query)
        hits = self._search.search(terms, limit=query.max_results)

        # Defense in depth (ADR-007 decision 3, enforcement place 3): the
        # source-file schema and the database CHECK constraint already keep
        # every stored row inside ALLOWED_TIERS, but a CorpusSearch
        # implementation is not assumed to guarantee it.
        in_policy = [hit for hit in hits if hit.source_tier in ALLOWED_TIERS]
        dropped = len(hits) - len(in_policy)
        if dropped:
            logger.warning(
                "curated corpus search returned %d hit(s) outside the tier "
                "policy; dropped before use",
                dropped,
            )

        if not in_policy:
            return []

        scored = [
            (hit, hit.rank + TIER_BONUS.get(hit.source_tier, 0.0))
            for hit in in_policy
        ]
        highest = max(score for _, score in scored) or 1.0

        # Total order -- score, then document_id, then chunk_id -- so an
        # unchanged corpus version answers an identical query identically
        # every time (AI-02b-5 determinism requirement).
        scored.sort(key=lambda pair: (-pair[1], pair[0].document_id, pair[0].chunk_id))

        logger.info(
            "curated corpus retrieval corpus_version=%s hits=%d",
            self.corpus_version,
            len(scored),
        )

        return [
            _to_retrieved_document(hit, round(min(score / highest, 1.0), 4))
            for hit, score in scored[: query.max_results]
        ]


__all__ = ["CorpusEvidenceRetriever"]

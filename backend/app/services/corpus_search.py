"""Adapter binding `CorpusRepository`'s SQL to the `CorpusSearch` protocol.

The one seam ADR-007 decision 5 requires: `app/ai/` depends on `CorpusSearch`
(`app/ai/providers/base.py`) and never imports `SessionLocal` directly. This
adapter is what `app/api/dependencies.py` constructs and passes to
`build_providers()` when `AI_RETRIEVAL_PROVIDER=corpus` -- the retriever
itself never sees a `Session`.
"""

from app.ai.corpus.policy import ALLOWED_TIERS
from app.ai.providers.base import CorpusHit, CorpusSearchTerms
from app.core.database import SessionLocal
from app.repositories.corpus_repository import CorpusRepository


class SessionCorpusSearch:
    """Opens one short-lived session per search call."""

    def __init__(self, repository: CorpusRepository | None = None):
        self._repository = repository or CorpusRepository()

    def search(self, terms: CorpusSearchTerms, *, limit: int) -> list[CorpusHit]:
        with SessionLocal() as db:
            return self._repository.search(db, terms, tiers=ALLOWED_TIERS, limit=limit)


__all__ = ["SessionCorpusSearch"]

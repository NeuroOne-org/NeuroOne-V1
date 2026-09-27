"""Provider selection.

The single place that maps configuration to concrete providers. Adding the
live LLM branch here was the whole of the AI-02a wiring (ADR-005); adding
the curated corpus branch is the whole of AI-02b's (ADR-007) -- nothing
downstream of the seam changes.
"""

from pathlib import Path

import httpx
from sqlalchemy.engine import make_url

from app.ai.corpus.source_schema import load_manifest
from app.ai.providers.base import CorpusSearch, EvidenceRetriever, ImagingStager, LLMClient
from app.ai.providers.corpus_retriever import CorpusEvidenceRetriever
from app.ai.providers.live_llm import LiveLLMClient
from app.ai.providers.mock_llm import MockLLMClient
from app.ai.providers.mock_retriever import MockEvidenceRetriever
from app.ai.providers.mock_staging import MockImagingStager
from app.core.config import Settings, settings


# backend/corpus/manifest.yaml, resolved from this file's location rather
# than the working directory, so build_providers() behaves the same whether
# the process is started from `backend/` or the repository root.
CORPUS_MANIFEST_PATH = Path(__file__).resolve().parents[3] / "corpus" / "manifest.yaml"


def _build_stager(config: Settings) -> ImagingStager:
    if config.AI_STAGING_PROVIDER == "mock":
        return MockImagingStager()

    raise ValueError(f"Unknown AI staging provider: {config.AI_STAGING_PROVIDER!r}")


def _corpus_version() -> str:
    """The active manifest's `corpus_version`, read fresh at build time.

    Not cached at import time: a developer re-ingesting a new version should
    not have to restart to pick up the new suffix (the API process still
    does, since `build_providers()` runs once at import in
    `app/api/dependencies.py`, but a test or script calling this function
    directly gets the current file).
    """

    return load_manifest(CORPUS_MANIFEST_PATH).corpus_version


def _build_retriever(
    config: Settings, corpus_search: CorpusSearch | None
) -> EvidenceRetriever:
    if config.AI_RETRIEVAL_PROVIDER == "mock":
        return MockEvidenceRetriever()

    if config.AI_RETRIEVAL_PROVIDER == "corpus":
        # Three refusals at startup, not mid-analysis (ADR-005 precedent,
        # ADR-007 decision 7): the mock reasoner cannot cite real corpus
        # documents; a live retriever needs a search backend; and a
        # Postgres-only feature needs a Postgres database.
        if config.AI_PROVIDER == "mock":
            raise ValueError(
                "AI_RETRIEVAL_PROVIDER='corpus' requires AI_PROVIDER='live-llm' "
                "-- the mock reasoner cannot cite real corpus documents, and "
                "the pipeline_note would misdescribe the analysis."
            )

        if corpus_search is None:
            raise ValueError(
                "AI_RETRIEVAL_PROVIDER='corpus' requires a CorpusSearch to be "
                "passed to build_providers(corpus_search=...)."
            )

        backend_name = make_url(config.DATABASE_URL).get_backend_name()
        if backend_name != "postgresql":
            raise ValueError(
                "AI_RETRIEVAL_PROVIDER='corpus' requires a Postgres "
                f"DATABASE_URL; got a {backend_name!r} URL. Set "
                "AI_RETRIEVAL_PROVIDER=mock, or point DATABASE_URL at "
                "Postgres."
            )

        return CorpusEvidenceRetriever(corpus_search, corpus_version=_corpus_version())

    raise ValueError(
        f"Unknown AI retrieval provider: {config.AI_RETRIEVAL_PROVIDER!r}"
    )


def build_providers(
    config: Settings | None = None,
    *,
    http_client: httpx.Client | None = None,
    corpus_search: CorpusSearch | None = None,
) -> tuple[EvidenceRetriever, LLMClient, ImagingStager]:
    """Return the (retriever, llm, stager) triple for the configured providers.

    `corpus_search` is only consulted when `AI_RETRIEVAL_PROVIDER=corpus`; it
    is `None` in every other configuration, including every existing test
    and the default `mock`/`mock` state, which is why this stays additive
    rather than a breaking signature change.
    """

    config = config or settings
    stager = _build_stager(config)
    retriever = _build_retriever(config, corpus_search)

    if config.AI_PROVIDER == "mock":
        return retriever, MockLLMClient(), stager

    if config.AI_PROVIDER == "live-llm":
        if not config.AI_LLM_API_KEY:
            # Fail where the misconfiguration is, rather than mid-analysis on
            # a clinician's screen (ADR-005).
            raise ValueError(
                "AI_PROVIDER='live-llm' requires AI_LLM_API_KEY. Set it in "
                "backend/.env, or set AI_PROVIDER=mock."
            )

        return retriever, LiveLLMClient(config, client=http_client), stager

    raise ValueError(f"Unknown AI provider: {config.AI_PROVIDER!r}")


__all__ = ["build_providers"]

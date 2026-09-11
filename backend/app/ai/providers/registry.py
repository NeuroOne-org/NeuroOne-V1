"""Provider selection.

The single place that maps configuration to concrete providers. Adding the
live branch here is the whole of the AI-02 wiring; nothing downstream of the
seam changes (ADR-003, ADR-005).
"""

import httpx

from app.ai.providers.base import EvidenceRetriever, LLMClient
from app.ai.providers.live_llm import LiveLLMClient
from app.ai.providers.mock_llm import MockLLMClient
from app.ai.providers.mock_retriever import MockEvidenceRetriever
from app.core.config import Settings, settings


def build_providers(
    config: Settings | None = None,
    *,
    http_client: httpx.Client | None = None,
) -> tuple[EvidenceRetriever, LLMClient]:
    """Return the (retriever, llm) pair for the configured provider."""

    config = config or settings

    if config.AI_PROVIDER == "mock":
        return MockEvidenceRetriever(), MockLLMClient()

    if config.AI_PROVIDER == "live-llm":
        if not config.AI_LLM_API_KEY:
            # Fail where the misconfiguration is, rather than mid-analysis on
            # a clinician's screen (ADR-005).
            raise ValueError(
                "AI_PROVIDER='live-llm' requires AI_LLM_API_KEY. Set it in "
                "backend/.env, or set AI_PROVIDER=mock."
            )

        # Retrieval stays simulated: AI-02 swaps the reasoning provider only,
        # which is why the two protocols were split (ADR-003).
        return (
            MockEvidenceRetriever(),
            LiveLLMClient(config, client=http_client),
        )

    raise ValueError(f"Unknown AI provider: {config.AI_PROVIDER!r}")


__all__ = ["build_providers"]

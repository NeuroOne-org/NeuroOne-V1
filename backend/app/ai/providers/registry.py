"""Provider selection.

The single place that maps configuration to concrete providers. AI-02 adds a
branch here and widens ``Settings.AI_PROVIDER``; nothing else in the pipeline
changes (ADR-003).
"""

from app.ai.providers.base import EvidenceRetriever, LLMClient
from app.ai.providers.mock_llm import MockLLMClient
from app.ai.providers.mock_retriever import MockEvidenceRetriever
from app.core.config import Settings, settings


def build_providers(
    config: Settings | None = None,
) -> tuple[EvidenceRetriever, LLMClient]:
    """Return the (retriever, llm) pair for the configured provider."""

    config = config or settings

    if config.AI_PROVIDER == "mock":
        return MockEvidenceRetriever(), MockLLMClient()

    raise ValueError(f"Unknown AI provider: {config.AI_PROVIDER!r}")


__all__ = ["build_providers"]

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    APP_NAME: str = "NeuroONE"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SQL_ECHO: bool = False

    # Providers sit behind app/ai/providers/base.py. "live-llm" is live
    # reasoning over a still-simulated corpus (ADR-004); real retrieval is a
    # later slice. The default stays "mock": live reasoning sends clinical
    # context to a third party, which section 12 permits only under the
    # unconfirmed synthetic-demo-data assumption.
    AI_PROVIDER: Literal["mock", "live-llm"] = "mock"
    AI_MAX_CANDIDATES: int = 5
    AI_EVIDENCE_PER_CANDIDATE: int = 3

    # Any OpenAI-compatible /chat/completions endpoint. Provider choice is
    # configuration rather than a code branch (ADR-004), so Groq, Gemini's
    # compatibility endpoint, OpenRouter and a local Ollama all work here.
    AI_LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    # Verify against the provider's own /models list when changing this --
    # hosted model ids are retired without notice, and a stale one is a 404.
    AI_LLM_MODEL: str = "openai/gpt-oss-120b"
    # Optional so mock mode boots without a key; build_providers() rejects a
    # live selection that has none.
    AI_LLM_API_KEY: str | None = None
    AI_LLM_TIMEOUT_SECONDS: float = 30.0
    AI_LLM_MAX_OUTPUT_TOKENS: int = 2048

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

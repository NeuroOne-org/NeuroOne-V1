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

    # Explicit allow-list, not a wildcard: the frontend sends the JWT via
    # Authorization header with credentialed requests, and CORS forbids
    # combining allow_origins=["*"] with allow_credentials=True anyway.
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Gmail SMTP sender for password-reset OTP emails (app/services/otp_service.py).
    # Optional so the API boots without them (e.g. under docker-compose);
    # sending an OTP is what fails when they are unset.
    GMAIL_ADDRESS: str | None = None
    GMAIL_APP_PASSWORD: str | None = None

    # Providers sit behind app/ai/providers/base.py. "live-llm" is live
    # reasoning over a still-simulated corpus (ADR-005); real retrieval is a
    # later slice. The default stays "mock": live reasoning sends clinical
    # context to a third party, which section 12 permits only under the
    # unconfirmed synthetic-demo-data assumption.
    AI_PROVIDER: Literal["mock", "live-llm"] = "mock"
    AI_MAX_CANDIDATES: int = 5
    AI_EVIDENCE_PER_CANDIDATE: int = 3

    # A third seam alongside AI_PROVIDER (ADR-006 decision 4): provenance is
    # now three-dimensional -- simulated retrieval, live-or-simulated
    # reasoning, simulated staging -- so a single literal no longer stretches
    # to cover it. "mock" is the only value until a live staging model exists.
    AI_STAGING_PROVIDER: Literal["mock"] = "mock"

    # Any OpenAI-compatible /chat/completions endpoint. Provider choice is
    # configuration rather than a code branch (ADR-005), so Groq, Gemini's
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

    # Where scan bytes live outside the database (ADR-006 decision 5). A
    # relative value resolves against the backend directory, matching
    # ENV_FILE below; an absolute path (e.g. a mounted volume) overrides it.
    SCAN_STORAGE_DIR: Path = ENV_FILE.parent / "storage" / "scans"
    MAX_SCAN_SIZE_BYTES: int = 200 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

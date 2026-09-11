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
    GMAIL_ADDRESS: str
    GMAIL_APP_PASSWORD: str

    # AI-01 ships mocked providers behind app/ai/providers/base.py.
    # AI-02 widens this literal; nothing else in the pipeline changes.
    AI_PROVIDER: Literal["mock"] = "mock"
    AI_MAX_CANDIDATES: int = 5
    AI_EVIDENCE_PER_CANDIDATE: int = 3

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

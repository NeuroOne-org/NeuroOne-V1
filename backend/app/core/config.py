from pathlib import Path

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

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

"""Startup safety checks on Settings (app/core/config.py)."""

import pytest

from app.core.config import Settings


def _base_kwargs(**overrides) -> dict:
    # GMAIL_* default to None here (rather than falling through to the
    # test-suite env vars set in conftest.py) so
    # test_refuses_email_delivery_without_gmail_credentials actually
    # exercises the missing-credentials case; tests that need real
    # credentials pass them explicitly.
    kwargs = dict(
        DATABASE_URL="sqlite+pysqlite:///:memory:",
        JWT_SECRET_KEY="test-secret",
        JWT_ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=30,
        GMAIL_ADDRESS=None,
        GMAIL_APP_PASSWORD=None,
        _env_file=None,
    )
    kwargs.update(overrides)
    return kwargs


def test_refuses_to_start_with_otp_off_in_production() -> None:
    with pytest.raises(ValueError, match="AUTH_REQUIRE_OTP must be true"):
        Settings(**_base_kwargs(APP_ENV="production", AUTH_REQUIRE_OTP=False))


def test_allows_otp_off_in_development() -> None:
    settings = Settings(
        **_base_kwargs(APP_ENV="development", AUTH_REQUIRE_OTP=False)
    )
    assert settings.AUTH_REQUIRE_OTP is False


def test_allows_otp_on_in_production() -> None:
    settings = Settings(
        **_base_kwargs(
            APP_ENV="production",
            AUTH_REQUIRE_OTP=True,
            OTP_DELIVERY="email",
            GMAIL_ADDRESS="a@example.com",
            GMAIL_APP_PASSWORD="app-password",
        )
    )
    assert settings.AUTH_REQUIRE_OTP is True


def test_refuses_email_delivery_without_gmail_credentials() -> None:
    with pytest.raises(ValueError, match="GMAIL_ADDRESS and GMAIL_APP_PASSWORD"):
        Settings(**_base_kwargs(OTP_DELIVERY="email"))


def test_console_delivery_does_not_require_gmail_credentials() -> None:
    settings = Settings(**_base_kwargs(OTP_DELIVERY="console"))
    assert settings.OTP_DELIVERY == "console"

"""Shared pytest configuration."""

from pathlib import Path
import os
import sys

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-only-jwt-secret")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("GMAIL_ADDRESS", "test-only@example.com")
os.environ.setdefault("GMAIL_APP_PASSWORD", "test-only-app-password")

# Most existing tests assert on the pre-2FA login contract (password in,
# token out) and construct their own OTP scenarios explicitly where needed,
# so the suite defaults to OTP off rather than the production-safe default.
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("AUTH_REQUIRE_OTP", "false")
os.environ.setdefault("OTP_DELIVERY", "console")

# Pin the provider, because an environment variable outranks the .env file
# and several suites call build_providers() with no argument. Without this, a
# developer with AI_PROVIDER=live-llm in backend/.env would have the test
# suite issue real, billable model calls and fail when offline. Tests that
# exercise the live provider construct their own Settings and drive an
# httpx.MockTransport.
os.environ["AI_PROVIDER"] = "mock"

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture(autouse=True)
def _clear_rate_limit_buckets():
    """The rate limiter (app/utils/rate_limit.py) is a process-global dict,
    so without this, unrelated tests that hit the same endpoint would share
    a window and spuriously start 429ing each other out."""

    from app.utils.rate_limit import _buckets

    _buckets.clear()
    yield
    _buckets.clear()

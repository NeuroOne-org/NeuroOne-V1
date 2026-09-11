"""Shared pytest configuration."""

from pathlib import Path
import os
import sys

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-only-jwt-secret")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("GMAIL_ADDRESS", "test-only@example.com")
os.environ.setdefault("GMAIL_APP_PASSWORD", "test-only-app-password")

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

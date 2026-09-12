"""Tests for the in-memory rate limiter (app/utils/rate_limit.py)."""

import pytest

from app.utils import rate_limit
from app.utils.exceptions import RateLimitedError


def test_allows_calls_up_to_the_limit() -> None:
    for _ in range(5):
        rate_limit.enforce("key-a", limit=5, window_seconds=60, message="nope")


def test_raises_once_the_limit_is_exceeded() -> None:
    for _ in range(5):
        rate_limit.enforce("key-b", limit=5, window_seconds=60, message="too many")

    with pytest.raises(RateLimitedError) as exc_info:
        rate_limit.enforce("key-b", limit=5, window_seconds=60, message="too many")

    assert exc_info.value.error_code == "rate_limited"
    assert exc_info.value.details["retry_after_seconds"] > 0


def test_a_blocked_key_does_not_keep_incrementing() -> None:
    """Calls made after the limit is hit must not count further, or the
    retry window would keep sliding forward under continued traffic."""

    for _ in range(5):
        rate_limit.enforce("key-f", limit=5, window_seconds=60, message="nope")

    for _ in range(3):
        with pytest.raises(RateLimitedError):
            rate_limit.enforce("key-f", limit=5, window_seconds=60, message="nope")

    assert rate_limit._buckets["key-f"].count == 5


def test_different_keys_do_not_share_a_bucket() -> None:
    for _ in range(5):
        rate_limit.enforce("key-c", limit=5, window_seconds=60, message="nope")

    # A different key has its own budget and is unaffected.
    rate_limit.enforce("key-d", limit=5, window_seconds=60, message="nope")


def test_window_resets_after_it_elapses(monkeypatch) -> None:
    now = [1_000.0]
    monkeypatch.setattr(rate_limit.time, "time", lambda: now[0])

    for _ in range(3):
        rate_limit.enforce("key-e", limit=3, window_seconds=10, message="nope")

    with pytest.raises(RateLimitedError):
        rate_limit.enforce("key-e", limit=3, window_seconds=10, message="nope")

    now[0] += 11
    # Does not raise: the window has rolled over.
    rate_limit.enforce("key-e", limit=3, window_seconds=10, message="nope")

# app/utils/rate_limit.py
#
# Fixed-window rate limiting for the auth endpoints (app/api/v1/auth.py):
# login, forgot-password, request-otp, verify-otp, reset-password.
#
# NOTE on storage: like the OTP store (app/services/otp_service.py), counts
# live in a simple in-memory dict. Fine for a single backend process, but
# it resets on restart and each process would keep its own counts. Move to
# a shared store (e.g. Redis) before running more than one instance.

import time
from dataclasses import dataclass, field

from fastapi import Request

from app.utils.exceptions import RateLimitedError


@dataclass
class _Window:
    count: int = 0
    started_at: float = field(default_factory=time.time)


# { key (e.g. "login:ip:1.2.3.4"): _Window }
_buckets: dict[str, _Window] = {}


def enforce(key: str, *, limit: int, window_seconds: float, message: str) -> None:
    """Records one attempt under `key` and raises RateLimitedError if that
    puts it over `limit` within the current `window_seconds` window.

    Every call counts, whether the request goes on to succeed or fail --
    otherwise the limit could be probed for free by only counting failures.
    """

    now = time.time()
    window = _buckets.get(key)
    if window is None or now - window.started_at >= window_seconds:
        window = _Window(started_at=now)
        _buckets[key] = window

    if window.count >= limit:
        retry_after = max(1, int(window.started_at + window_seconds - now) + 1)
        raise RateLimitedError(
            message,
            details={"retry_after_seconds": retry_after},
        )

    window.count += 1


def client_ip(request: Request) -> str:
    """Best-effort source IP for keying per-IP limits.

    Reads only `request.client.host` -- there is no reverse proxy in front
    of this backend today, so an X-Forwarded-For header would be
    client-supplied and trivially spoofable. Add trusted-proxy handling
    here if one is introduced later.
    """

    return request.client.host if request.client else "unknown"

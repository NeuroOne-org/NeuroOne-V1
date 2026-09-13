"""The browser session cookie.

The access token reaches the browser only as an HttpOnly cookie, so page
scripts -- and therefore any XSS payload -- can never read it. Non-browser
clients can still present the same token as an ``Authorization: Bearer``
header (see ``get_current_user``).
"""

from starlette.responses import Response

from app.core.config import settings


SESSION_COOKIE_NAME = "neuroone_session"

# Cookie-authenticated writes must carry this header. The browser attaches the
# cookie on its own, but a cross-site form or link cannot set a custom header,
# and a cross-origin script that tries is stopped at the CORS preflight. That
# covers the same-site sibling origins SameSite=Strict still lets through.
CSRF_HEADER_NAME = "X-Requested-With"
CSRF_HEADER_VALUE = "XMLHttpRequest"


def set_session_cookie(response: Response, token: str) -> None:
    """Attach the access token to a response as the session cookie."""

    response.set_cookie(
        SESSION_COOKIE_NAME,
        token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        secure=settings.SESSION_COOKIE_SECURE,
        httponly=True,
        samesite="strict",
    )


def clear_session_cookie(response: Response) -> None:
    """Expire the session cookie. Attributes match set_session_cookie."""

    response.delete_cookie(
        SESSION_COOKIE_NAME,
        path="/",
        secure=settings.SESSION_COOKIE_SECURE,
        httponly=True,
        samesite="strict",
    )

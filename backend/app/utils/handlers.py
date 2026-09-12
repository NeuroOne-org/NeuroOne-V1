"""Global translation of domain exceptions into HTTP responses."""

import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import ErrorResponse
from app.utils.exceptions import (
    AIError,
    ApplicationError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DatabaseError,
    ExternalServiceError,
    InternalServerError,
    NotFoundError,
    RateLimitedError,
    ValidationApplicationError,
)

logger = logging.getLogger(__name__)


def _error_response(
    status_code: int,
    message: str,
    error_code: str | None = None,
    *,
    details: object | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    payload = ErrorResponse(
        message=message,
        error_code=error_code,
        details=jsonable_encoder(details) if details is not None else None,
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(),
        headers=headers,
    )


def _application_handler(status_code: int, *, authenticate: bool = False):
    async def handler(request: Request, exc: ApplicationError) -> JSONResponse:
        headers = {"WWW-Authenticate": "Bearer"} if authenticate else None
        return _error_response(
            status_code,
            exc.message,
            exc.error_code,
            details=exc.details,
            headers=headers,
        )

    return handler


async def rate_limited_handler(request: Request, exc: RateLimitedError) -> JSONResponse:
    retry_after = (
        exc.details.get("retry_after_seconds") if isinstance(exc.details, dict) else None
    )
    headers = {"Retry-After": str(retry_after)} if retry_after is not None else None
    return _error_response(
        429,
        exc.message,
        exc.error_code,
        details=exc.details,
        headers=headers,
    )


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return _error_response(
        422,
        "Request validation failed.",
        "validation_error",
        details=exc.errors(),
    )


async def validation_error_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    return _error_response(
        422,
        "Validation failed.",
        "validation_error",
        details=exc.errors(),
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    error_codes = {
        401: "authentication_error",
        403: "authorization_error",
        404: "not_found",
        409: "conflict",
    }
    message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    return _error_response(
        exc.status_code,
        message,
        error_codes.get(exc.status_code, "http_error"),
        details=None if isinstance(exc.detail, str) else exc.detail,
        headers=exc.headers,
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled application error", exc_info=exc)
    return _error_response(
        500,
        "An unexpected error occurred.",
        "internal_server_error",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register every centralized domain-to-HTTP mapping."""

    app.add_exception_handler(ValidationApplicationError, _application_handler(422))
    app.add_exception_handler(
        AuthenticationError,
        _application_handler(401, authenticate=True),
    )
    app.add_exception_handler(AuthorizationError, _application_handler(403))
    app.add_exception_handler(NotFoundError, _application_handler(404))
    app.add_exception_handler(ConflictError, _application_handler(409))
    app.add_exception_handler(DatabaseError, _application_handler(503))
    app.add_exception_handler(AIError, _application_handler(502))
    app.add_exception_handler(ExternalServiceError, _application_handler(502))
    app.add_exception_handler(InternalServerError, _application_handler(500))
    app.add_exception_handler(RateLimitedError, rate_limited_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)


__all__ = ["register_exception_handlers"]

"""Global translation of domain exceptions into HTTP responses."""

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.utils.exceptions import (
    AuthenticationError,
    AuthorizationError,
    EntityNotFoundError,
    UserAlreadyExistsError,
)


def _error_response(
    status_code: int,
    detail: object,
    *,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"detail": jsonable_encoder(detail)},
        headers=headers,
    )


async def entity_not_found_handler(
    request: Request,
    exc: EntityNotFoundError,
) -> JSONResponse:
    return _error_response(404, str(exc))


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
) -> JSONResponse:
    return _error_response(409, str(exc))


async def authentication_error_handler(
    request: Request,
    exc: AuthenticationError,
) -> JSONResponse:
    return _error_response(
        401,
        str(exc),
        headers={"WWW-Authenticate": "Bearer"},
    )


async def authorization_error_handler(
    request: Request,
    exc: AuthorizationError,
) -> JSONResponse:
    return _error_response(403, str(exc))


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return _error_response(422, exc.errors())


async def validation_error_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    return _error_response(422, exc.errors())


def register_exception_handlers(app: FastAPI) -> None:
    """Register all application-wide exception mappings."""

    app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(AuthorizationError, authorization_error_handler)
    app.add_exception_handler(
        RequestValidationError,
        request_validation_error_handler,
    )
    app.add_exception_handler(ValidationError, validation_error_handler)


__all__ = ["register_exception_handlers"]

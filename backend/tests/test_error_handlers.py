"""Coverage for the complete centralized error-category contract."""

from typing import ClassVar

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app
from app.schemas.common import ErrorResponse
from app.utils.exceptions import (
    AIError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DatabaseError,
    ExternalServiceError,
    InternalServerError,
    NotFoundError,
    ValidationApplicationError,
)
from app.utils import handlers
from app.utils.handlers import register_exception_handlers


def test_all_required_domain_error_categories_are_registered() -> None:
    categories = {
        ValidationApplicationError,
        AuthenticationError,
        AuthorizationError,
        NotFoundError,
        ConflictError,
        DatabaseError,
        AIError,
        ExternalServiceError,
        InternalServerError,
    }

    assert categories.issubset(app.exception_handlers)


def test_error_response_helper_instantiates_declared_model(monkeypatch) -> None:
    class TrackingErrorResponse(ErrorResponse):
        constructed: ClassVar[bool] = False

        def __init__(self, **data) -> None:
            super().__init__(**data)
            type(self).constructed = True

    monkeypatch.setattr(handlers, "ErrorResponse", TrackingErrorResponse)

    response = handlers._error_response(
        503,
        "Unable to create record.",
        "database_error",
    )

    assert TrackingErrorResponse.constructed
    assert response.body == (
        b'{"message":"Unable to create record.",'
        b'"error_code":"database_error","details":null}'
    )


@pytest.mark.parametrize(
    ("error_type", "expected_status", "expected_code"),
    [
        (ValidationApplicationError, 422, "validation_error"),
        (AuthenticationError, 401, "authentication_error"),
        (AuthorizationError, 403, "authorization_error"),
        (NotFoundError, 404, "not_found"),
        (ConflictError, 409, "conflict"),
        (DatabaseError, 503, "database_error"),
        (AIError, 502, "ai_error"),
        (ExternalServiceError, 502, "external_service_error"),
        (InternalServerError, 500, "internal_server_error"),
    ],
)
def test_every_domain_error_serializes_the_declared_error_response_shape(
    error_type,
    expected_status: int,
    expected_code: str,
) -> None:
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/error")
    def raise_error():
        raise error_type("Synthetic failure.")

    response = TestClient(test_app, raise_server_exceptions=False).get("/error")
    body = response.json()

    assert response.status_code == expected_status
    assert list(body) == list(ErrorResponse.model_fields)
    assert body == {
        "message": "Synthetic failure.",
        "error_code": expected_code,
        "details": None,
    }
    ErrorResponse.model_validate(body)

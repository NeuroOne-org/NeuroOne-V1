"""HTTP-agnostic application exception hierarchy."""

from typing import Any


class ApplicationError(Exception):
    default_error_code = "application_error"

    def __init__(
        self,
        message: str,
        *,
        error_code: str | None = None,
        details: dict[str, Any] | list[Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.default_error_code
        self.details = details


class ValidationApplicationError(ApplicationError):
    default_error_code = "validation_error"


class AuthenticationError(ApplicationError):
    default_error_code = "authentication_error"


class AuthorizationError(ApplicationError):
    default_error_code = "authorization_error"


class NotFoundError(ApplicationError):
    default_error_code = "not_found"


class ConflictError(ApplicationError):
    default_error_code = "conflict"


class DatabaseError(ApplicationError):
    default_error_code = "database_error"


class AIError(ApplicationError):
    default_error_code = "ai_error"


class ExternalServiceError(ApplicationError):
    default_error_code = "external_service_error"


class InternalServerError(ApplicationError):
    default_error_code = "internal_server_error"


class InvalidCredentialsError(AuthenticationError):
    """Raised when supplied login credentials are invalid."""


class UserAlreadyExistsError(ConflictError):
    """Raised when a unique user identity is already registered."""


class InvalidOtpError(ValidationApplicationError):
    """Raised when a submitted OTP is wrong, expired, or unknown."""

    default_error_code = "invalid_otp"


class EntityNotFoundError(NotFoundError):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity: str, identifier: object | None = None):
        self.entity = entity
        self.identifier = identifier
        message = f"{entity} not found."
        if identifier is not None:
            message = f"{entity} with ID '{identifier}' not found."
        super().__init__(message)


class AnalysisNotReviewedError(ConflictError):
    """Raised when a report is requested for an unreviewed analysis.

    ADR-006 decision 6: sign-off gates the report, structurally rather than
    as a disclaimer.
    """

    default_error_code = "analysis_not_reviewed"


__all__ = [
    "AIError",
    "AnalysisNotReviewedError",
    "ApplicationError",
    "AuthenticationError",
    "AuthorizationError",
    "ConflictError",
    "DatabaseError",
    "EntityNotFoundError",
    "ExternalServiceError",
    "InternalServerError",
    "InvalidCredentialsError",
    "InvalidOtpError",
    "NotFoundError",
    "UserAlreadyExistsError",
    "ValidationApplicationError",
]

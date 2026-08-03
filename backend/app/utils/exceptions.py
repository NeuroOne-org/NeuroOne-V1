"""Application-specific exceptions."""


class ApplicationError(Exception):
    """Base class for application-level failures."""


class AuthenticationError(ApplicationError):
    """Raised when authentication cannot be completed."""


class AuthorizationError(ApplicationError):
    """Raised when an authenticated user lacks permission."""


class UserAlreadyExistsError(ApplicationError):
    """Raised when a unique user identity is already registered."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when supplied login credentials are invalid."""


class EntityNotFoundError(ApplicationError):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity: str, identifier: object | None = None):
        self.entity = entity
        self.identifier = identifier

        message = f"{entity} not found."
        if identifier is not None:
            message = f"{entity} with ID '{identifier}' not found."

        super().__init__(message)


__all__ = [
    "ApplicationError",
    "AuthenticationError",
    "AuthorizationError",
    "EntityNotFoundError",
    "InvalidCredentialsError",
    "UserAlreadyExistsError",
]

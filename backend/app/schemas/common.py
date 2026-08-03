"""Schemas shared across application features."""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """A simple response containing a human-readable message."""

    message: str


class ErrorResponse(BaseModel):
    """The standard shape returned for API errors."""

    message: str
    error_code: str | None = None
    details: dict[str, Any] | list[Any] | None = None


class Pagination(BaseModel):
    """Pagination metadata returned with collection responses."""

    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_records: int = Field(ge=0)
    total_pages: int = Field(ge=0)


ResponseType = TypeVar("ResponseType")


class PaginatedResponse(BaseModel, Generic[ResponseType]):
    """Generic response wrapper for paginated collection endpoints."""

    items: list[ResponseType]
    pagination: Pagination


__all__ = [
    "ErrorResponse",
    "MessageResponse",
    "PaginatedResponse",
    "Pagination",
]

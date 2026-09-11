"""Scan wire schema (ADR-006).

No storage_key: that is an internal reference into the storage backend, not
something a client needs, and exposing it would leak filesystem layout.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ScanResponse(BaseModel):
    """A persisted scan's metadata, as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    visit_id: UUID
    uploaded_by_id: UUID
    original_filename: str
    content_type: str
    size_bytes: int
    checksum: str
    dimensions: dict[str, Any] = Field(default_factory=dict)
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime


__all__ = ["ScanResponse"]

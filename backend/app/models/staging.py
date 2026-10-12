"""Persisted imaging-staging results (ADR-008 risk: per-process cache).

A stage is a function of the scan's pixels and the model that read them, so
it is keyed by (checksum, model_name) rather than by scan or visit: the same
bytes uploaded twice share one result, and switching staging model stages
again instead of serving the old model's answer. Holds no PHI -- a checksum
and a stage, never a storage key or filename.

Not a `BaseModel` subclass, like `CorpusDocument`: a result is never edited
or soft-deleted, only written once and read back.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, UUID, DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class StagingRecord(Base):
    """One staging model's result for one scan's bytes."""

    __tablename__ = "staging_results"
    __table_args__ = (UniqueConstraint("checksum", "model_name"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # A serialized StagingResult, re-validated on every read.
    result: Mapped[dict[str, Any]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


__all__ = ["StagingRecord"]

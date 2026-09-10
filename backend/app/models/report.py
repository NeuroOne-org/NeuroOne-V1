"""Immutable snapshot of a generated clinical report (ADR-004)."""

from datetime import datetime
from typing import Any
import uuid

from sqlalchemy import JSON, UUID, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


"""
+----------------------+
|       REPORT         |
+----------------------+
| PK id                |
| FK analysis_id       |
| FK generated_by_id   |
| generated_at         |
| filename             |
| snapshot             |
+----------------------+
"""


class Report(BaseModel):
    """One generated PDF report, snapshotting its source analysis.

    Never mutated after creation -- regenerating a report for the same
    analysis creates a new row. The PDF itself is not stored, only the typed
    snapshot it was (and will again be) rendered from: a download re-renders
    rather than reading stale bytes back, and no PHI-bearing PDF sits on a
    container filesystem (ADR-004).
    """

    __tablename__ = "reports"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id"),
        nullable=False,
        index=True,
    )
    generated_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(String(100), nullable=False)

    # Everything the renderer is allowed to see (ReportSnapshot), captured at
    # generation time. A later edit to the analysis, visit, or patient must
    # never change what an already-generated report says (ADR-004).
    snapshot: Mapped[dict[str, Any]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
    )


__all__ = ["Report"]

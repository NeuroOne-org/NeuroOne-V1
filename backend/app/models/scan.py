"""MRI scan metadata for a visit (ADR-006).

The scan's bytes are not a column here -- they live in file or object
storage, referenced by ``storage_key``. A PDF can be regenerated from its
snapshot (ADR-004); a scan cannot, so what is persisted is the reference,
its dimensions, and a checksum, not the image itself.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any
import uuid

from sqlalchemy import JSON, UUID, BigInteger, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .visit import Visit


"""
+----------------------+
|        SCAN          |
+----------------------+
| PK id                |
| FK visit_id (unique) |
| FK uploaded_by_id    |
| storage_key          |
| original_filename    |
| content_type         |
| size_bytes           |
| checksum             |
| dimensions           |
| uploaded_at          |
+----------------------+
"""


class Scan(BaseModel):
    """One MRI scan attached to a visit.

    Attaches to the Visit, not the Patient (ADR-006 decision 2): cross-visit
    comparison then falls out of the existing per-visit trend machinery
    instead of needing its own history model. One scan per visit -- a
    follow-up scan is a new visit's scan, not a replacement of this row.
    """

    __tablename__ = "scans"

    # ForeignKeys
    visit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("visits.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    visit: Mapped["Visit"] = relationship(
        "Visit",
        back_populates="scan",
    )

    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Reference into the storage backend, not the bytes themselves.
    storage_key: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # sha256 hex digest. The scan is source data that cannot be regenerated,
    # so integrity is checked against this rather than trusted on read.
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)

    # Free-form rather than fixed width/height columns: a DICOM series has a
    # slice count that a flat image does not, and this is descriptive
    # metadata, never filtered or queried, matching the vitals precedent on
    # Visit.
    dimensions: Mapped[dict[str, Any]] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False,
        default=dict,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


__all__ = ["Scan"]

"""Triage queue wire schema (ADR-006).

No stat tiles: this is a ranked queue, not an aggregate dashboard. Each entry
is a boolean read of the patient's most recent analysis, never a number that
could be mistaken for a clinical measurement (FR-04) -- an aggregate
confidence average across patients would be both clinically meaningless and
a step back toward the framing FR-04 forbids.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.common import PaginatedResponse


class TriageEntry(BaseModel):
    """One patient's position in the triage queue.

    Not an ORM-backed response: there is no single row this comes from, so
    the service builds this directly rather than a repository returning it
    for ``.model_validate()`` to narrow (the same reason ``ClinicalContext``
    and ``AnalysisResult`` are constructed rather than validated from a row).
    """

    model_config = ConfigDict(extra="forbid")

    patient_id: UUID
    patient_first_name: str
    patient_last_name: str | None = None

    # Ranked in exactly this order (ADR-006 decision 7).
    has_open_early_watch: bool
    has_worsening_trend: bool
    awaiting_sign_off: bool

    latest_visit_id: UUID | None = None
    latest_analysis_id: UUID | None = None
    latest_analysis_generated_at: datetime | None = None


class TriageListResponse(PaginatedResponse[TriageEntry]):
    """Paginated, ranked triage queue returned by the triage endpoint."""


__all__ = ["TriageEntry", "TriageListResponse"]

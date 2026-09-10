"""Report item endpoints.

Flat rather than nested under the analysis: a report id is globally unique,
so carrying the analysis id would be redundant, mirroring analysis.py's own
reasoning for staying flat relative to visits. Collection and generation
endpoints live in analysis.py, where the analysis is the natural parent.

A report reached by its own id gets a 404 labelled "Report" even when the
real cause is that its parent analysis belongs to another clinician --
otherwise the analysis's UUID would leak (ADR-002, applied two levels deeper).
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_active_user,
    get_db,
    get_report_service,
)
from app.models.report import Report
from app.models.user import User
from app.schemas.report import ReportResponse
from app.services.report_service import ReportService

router = APIRouter()


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
) -> Report:
    """Retrieve one report's metadata. Ownership violations read as 404."""

    return report_service.get_report(db, report_id, current_user)


@router.get("/{report_id}/pdf")
def download_report_pdf(
    report_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
) -> Response:
    """Stream the report's PDF, re-rendered from its immutable snapshot.

    Never cached: a report can carry patient data, so every response is
    marked private/no-store (AGENTS.md section 12).
    """

    pdf_bytes, filename = report_service.get_pdf(db, report_id, current_user)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "private, no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )

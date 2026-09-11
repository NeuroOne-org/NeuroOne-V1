"""Analysis item endpoints.

Flat rather than nested under the visit: an analysis id is globally unique, so
carrying the visit id would be redundant. Collection and trigger endpoints live
in visits.py, where the case is the natural parent.

An analysis reached by its own id gets a 404 labelled "Analysis" even when the
real cause is that its parent visit belongs to another clinician -- otherwise
the visit's UUID would leak (ADR-002, applied one level deeper).
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_analysis_service,
    get_current_active_user,
    get_db,
    get_report_service,
)
from app.models.analysis import Analysis
from app.models.report import Report
from app.models.user import User
from app.schemas.analysis import AnalysisResponse
from app.schemas.report import ReportListResponse, ReportResponse
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService
from app.utils.responses import build_pagination

router = APIRouter()


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
) -> Analysis:
    """Retrieve one analysis. Ownership violations read as 404."""

    return analysis_service.get_analysis(db, analysis_id, current_user)


@router.post("/{analysis_id}/review", response_model=AnalysisResponse)
def sign_off_analysis(
    analysis_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
) -> Analysis:
    """Record clinician sign-off. Gates report generation (ADR-006)."""

    return analysis_service.sign_off_analysis(db, analysis_id, current_user)


# --------------------------------------------------------------------------
# Reports (REPORT-01)
# --------------------------------------------------------------------------


@router.post(
    "/{analysis_id}/reports",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    analysis_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
) -> Report:
    """Generate a new report snapshot for an analysis.

    The PDF is proved to render before anything is persisted (ADR-004); the
    bytes themselves are fetched separately via ``GET /reports/{id}/pdf``.
    """

    return report_service.generate_report(db, analysis_id, current_user)


@router.get("/{analysis_id}/reports", response_model=ReportListResponse)
def list_reports(
    analysis_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ReportListResponse:
    """List an analysis's generated reports, newest first."""

    skip = (page - 1) * page_size
    items, total = report_service.list_analysis_reports(
        db, analysis_id, current_user, skip, page_size
    )
    return ReportListResponse(
        items=[ReportResponse.model_validate(item) for item in items],
        pagination=build_pagination(total, page, page_size),
    )

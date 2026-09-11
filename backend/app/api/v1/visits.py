"""Visit endpoints.

Item-level operations are flat rather than nested under the patient: a visit id
is globally unique, so carrying the patient id would be redundant and would
manufacture mismatched-pair routes. Collection and history endpoints live in
patient_visits.py, where the patient is the natural parent.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_analysis_service,
    get_current_active_user,
    get_db,
    get_scan_service,
    get_visit_service,
)
from app.models.analysis import Analysis
from app.models.scan import Scan
from app.models.symptom import Symptom
from app.models.user import User
from app.models.visit import Visit
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisListResponse,
    AnalysisResponse,
)
from app.schemas.scan import ScanResponse
from app.schemas.symptom import (
    SymptomCreate,
    SymptomListResponse,
    SymptomResponse,
    SymptomUpdate,
)
from app.schemas.visit import VisitResponse, VisitUpdate
from app.services.analysis_service import AnalysisService
from app.services.scan_service import ScanService
from app.services.visit_service import VisitService
from app.utils.responses import build_pagination

router = APIRouter()


def _analysis_page(
    items: list[Analysis],
    total: int,
    page: int,
    page_size: int,
) -> AnalysisListResponse:
    return AnalysisListResponse(
        items=[AnalysisResponse.model_validate(item) for item in items],
        pagination=build_pagination(total, page, page_size),
    )


def _symptom_page(
    items: list[Symptom],
    total: int,
    page: int,
    page_size: int,
) -> SymptomListResponse:
    return SymptomListResponse(
        items=[SymptomResponse.model_validate(item) for item in items],
        pagination=build_pagination(total, page, page_size),
    )


@router.get("/{visit_id}", response_model=VisitResponse)
def get_visit(
    visit_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
) -> Visit:
    """Retrieve a visit by ID. Ownership violations read as 404 (ADR-001/002)."""

    return visit_service.get_visit(db, visit_id, current_user)


@router.patch("/{visit_id}", response_model=VisitResponse)
def update_visit(
    visit_id: UUID,
    payload: VisitUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
) -> Visit:
    """Partially update a visit. Ownership violations read as 404."""

    return visit_service.update_visit(db, visit_id, payload, current_user)


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_visit(
    visit_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
) -> None:
    """Soft-delete a visit and its symptoms. Ownership violations read as 404."""

    visit_service.delete_visit(db, visit_id, current_user)


@router.get("/{visit_id}/symptoms", response_model=SymptomListResponse)
def list_symptoms(
    visit_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SymptomListResponse:
    """List the symptoms recorded against a visit."""

    skip = (page - 1) * page_size
    items, total = visit_service.list_symptoms(
        db, visit_id, current_user, skip, page_size
    )
    return _symptom_page(items, total, page, page_size)


@router.post(
    "/{visit_id}/symptoms",
    response_model=SymptomResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_symptom(
    visit_id: UUID,
    payload: SymptomCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
) -> Symptom:
    """Record a symptom against a visit."""

    return visit_service.add_symptom(db, visit_id, payload, current_user)


@router.patch("/{visit_id}/symptoms/{symptom_id}", response_model=SymptomResponse)
def update_symptom(
    visit_id: UUID,
    symptom_id: UUID,
    payload: SymptomUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
) -> Symptom:
    """Partially update a symptom. A symptom on another visit reads as 404."""

    return visit_service.update_symptom(
        db, visit_id, symptom_id, payload, current_user
    )


@router.delete(
    "/{visit_id}/symptoms/{symptom_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_symptom(
    visit_id: UUID,
    symptom_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
) -> None:
    """Soft-delete a symptom. A symptom on another visit reads as 404."""

    visit_service.delete_symptom(db, visit_id, symptom_id, current_user)


# --------------------------------------------------------------------------
# Scan (ADR-006)
# --------------------------------------------------------------------------


@router.post(
    "/{visit_id}/scan",
    response_model=ScanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_scan(
    visit_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    scan_service: Annotated[ScanService, Depends(get_scan_service)],
    file: Annotated[UploadFile, File()],
) -> Scan:
    """Attach an MRI scan to a visit. One scan per visit (ADR-006).

    Intake for a returning patient's follow-up scan is a new visit, not a
    replacement of this one -- that is what makes cross-visit comparison
    possible.
    """

    content = await file.read()
    return scan_service.upload_scan(
        db,
        visit_id,
        current_user,
        filename=file.filename or "scan",
        content_type=file.content_type or "application/octet-stream",
        content=content,
    )


@router.get("/{visit_id}/scan", response_model=ScanResponse)
def get_scan(
    visit_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    scan_service: Annotated[ScanService, Depends(get_scan_service)],
) -> Scan:
    """Retrieve the scan attached to a visit, if any."""

    return scan_service.get_scan(db, visit_id, current_user)


# --------------------------------------------------------------------------
# Analysis (AI-01)
# --------------------------------------------------------------------------


@router.post(
    "/{visit_id}/analyses",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_analysis(
    visit_id: UUID,
    payload: AnalysisCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
) -> Analysis:
    """Run the AI pipeline for a case and store the ranked result.

    Decision support only. An AI or retrieval failure returns 502 and leaves the
    clinical record untouched (AGENTS.md section 8.5).
    """

    return analysis_service.analyze_visit(
        db, visit_id, current_user, history_limit=payload.history_limit
    )


@router.get("/{visit_id}/analyses/latest", response_model=AnalysisResponse)
def get_latest_analysis(
    visit_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
) -> Analysis:
    """Return the most recent analysis for a case."""

    return analysis_service.get_latest_for_visit(db, visit_id, current_user)


@router.get("/{visit_id}/analyses", response_model=AnalysisListResponse)
def list_analyses(
    visit_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> AnalysisListResponse:
    """List a case's analyses, newest first."""

    skip = (page - 1) * page_size
    items, total = analysis_service.list_visit_analyses(
        db, visit_id, current_user, skip, page_size
    )
    return _analysis_page(items, total, page, page_size)

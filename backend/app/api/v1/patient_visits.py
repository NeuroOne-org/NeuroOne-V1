"""Patient-scoped visit endpoints.

Collections nest under the patient, matching APP-FLOW section 3 (Profile ->
Cases / History) and making the ownership target explicit in the path. Because
the caller names the patient here, a patient-level 404 keeps its honest label
rather than being masked to a Visit -- see ADR-002.
"""

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db, get_visit_service
from app.models.user import User
from app.models.visit import Visit, VisitStatus
from app.schemas.visit import (
    VisitCreate,
    VisitHistoryResponse,
    VisitListResponse,
    VisitResponse,
)
from app.services.visit_service import VisitService
from app.utils.responses import build_pagination

router = APIRouter()


def _visit_page(
    items: list[Visit],
    total: int,
    page: int,
    page_size: int,
) -> VisitListResponse:
    return VisitListResponse(
        items=[VisitResponse.model_validate(item) for item in items],
        pagination=build_pagination(total, page, page_size),
    )


@router.post(
    "/{patient_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_visit(
    patient_id: UUID,
    payload: VisitCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
) -> Visit:
    """Open a clinical case for a patient, optionally with symptoms inline."""

    return visit_service.create_visit(db, patient_id, payload, current_user)


@router.get("/{patient_id}/visits/history", response_model=VisitHistoryResponse)
def get_visit_history(
    patient_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    order: Annotated[Literal["asc", "desc"], Query()] = "desc",
    exclude_visit_id: Annotated[UUID | None, Query()] = None,
) -> VisitHistoryResponse:
    """Return a patient's visit history ordered for cross-visit comparison.

    A bounded window rather than a paginated collection: page numbers are
    meaningless alongside exclude_visit_id.
    """

    visits, total = visit_service.get_patient_history(
        db,
        patient_id,
        current_user,
        limit=limit,
        newest_first=order == "desc",
        exclude_visit_id=exclude_visit_id,
    )

    return VisitHistoryResponse(
        patient_id=patient_id,
        total_visits=total,
        returned=len(visits),
        order=order,
        visits=[VisitResponse.model_validate(visit) for visit in visits],
    )


@router.get("/{patient_id}/visits", response_model=VisitListResponse)
def list_patient_visits(
    patient_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    visit_service: Annotated[VisitService, Depends(get_visit_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    visit_status: Annotated[VisitStatus | None, Query(alias="status")] = None,
) -> VisitListResponse:
    """List a patient's visits, newest first."""

    skip = (page - 1) * page_size
    items, total = visit_service.list_patient_visits(
        db, patient_id, current_user, skip, page_size, visit_status
    )
    return _visit_page(items, total, page, page_size)

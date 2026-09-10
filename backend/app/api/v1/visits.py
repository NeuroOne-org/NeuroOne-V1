"""Visit endpoints.

Item-level operations are flat rather than nested under the patient: a visit id
is globally unique, so carrying the patient id would be redundant and would
manufacture mismatched-pair routes. Collection and history endpoints live in
patient_visits.py, where the patient is the natural parent.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db, get_visit_service
from app.models.symptom import Symptom
from app.models.user import User
from app.models.visit import Visit
from app.schemas.symptom import (
    SymptomCreate,
    SymptomListResponse,
    SymptomResponse,
    SymptomUpdate,
)
from app.schemas.visit import VisitResponse, VisitUpdate
from app.services.visit_service import VisitService
from app.utils.responses import build_pagination

router = APIRouter()


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

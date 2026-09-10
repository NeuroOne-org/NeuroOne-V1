"""Patient endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db, get_patient_service
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import (
    PatientCreate,
    PatientListResponse,
    PatientResponse,
    PatientUpdate,
)
from app.services.patient_service import PatientService
from app.utils.responses import build_pagination

router = APIRouter()


def _paginated_response(
    items: list[Patient],
    total: int,
    page: int,
    page_size: int,
) -> PatientListResponse:
    return PatientListResponse(
        items=[PatientResponse.model_validate(item) for item in items],
        pagination=build_pagination(total, page, page_size),
    )


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    payload: PatientCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    patient_service: Annotated[PatientService, Depends(get_patient_service)],
) -> Patient:
    """Create a patient, deriving/validating ownership by role."""

    return patient_service.create_patient(db, payload, current_user)


@router.get("", response_model=PatientListResponse)
def list_patients(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    patient_service: Annotated[PatientService, Depends(get_patient_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    doctor_id: Annotated[UUID | None, Query()] = None,
) -> PatientListResponse:
    """List patients, scoped to the caller's role (ADMIN may filter by doctor)."""

    skip = (page - 1) * page_size
    items, total = patient_service.list_patients(
        db, current_user, skip, page_size, doctor_id
    )
    return _paginated_response(items, total, page, page_size)


@router.get("/search", response_model=PatientListResponse)
def search_patients(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    patient_service: Annotated[PatientService, Depends(get_patient_service)],
    q: Annotated[str, Query()] = "",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PatientListResponse:
    """Search patients by name, email, or phone, scoped to the caller's role."""

    skip = (page - 1) * page_size
    items, total = patient_service.search_patients(
        db, q, current_user, skip, page_size
    )
    return _paginated_response(items, total, page, page_size)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    patient_service: Annotated[PatientService, Depends(get_patient_service)],
) -> Patient:
    """Retrieve a patient by ID. Ownership violations read as 404 (ADR-001)."""

    return patient_service.get_patient(db, patient_id, current_user)


@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: UUID,
    payload: PatientUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    patient_service: Annotated[PatientService, Depends(get_patient_service)],
) -> Patient:
    """Partially update a patient. Ownership violations read as 404 (ADR-001)."""

    return patient_service.update_patient(db, patient_id, payload, current_user)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    patient_service: Annotated[PatientService, Depends(get_patient_service)],
) -> None:
    """Soft-delete a patient. Ownership violations read as 404 (ADR-001)."""

    patient_service.delete_patient(db, patient_id, current_user)

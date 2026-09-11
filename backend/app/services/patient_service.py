"""Business logic for patient management."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Patient, User
from app.models.patient import PhoneNumber
from app.models.user import UserRole
from app.repositories.patient_repository import PatientRepository
from app.repositories.user_repository import UserRepository
from app.schemas.patient import PatientCreate, PatientUpdate
from app.services.base_service import BaseService
from app.utils.exceptions import (
    AuthorizationError,
    EntityNotFoundError,
    ValidationApplicationError,
)


class PatientService(BaseService[PatientRepository]):
    """Business logic for patient management."""

    def __init__(
        self,
        repository: PatientRepository,
        user_repository: UserRepository,
    ):
        super().__init__(repository)
        self.user_repository = user_repository

    def _authorize_access(self, patient: Patient, current_user: User) -> None:
        """Ensure the current user may access this patient.

        Per ADR-001, an ownership violation is indistinguishable from the
        patient not existing: both raise EntityNotFoundError (-> 404), so a
        caller with no legitimate claim to the record can't tell the two
        cases apart.
        """
        if current_user.role == UserRole.ADMIN:
            return
        if patient.doctor_id != current_user.id:
            raise EntityNotFoundError("Patient", patient.id)

    def _validate_doctor(self, db: Session, doctor_id: UUID) -> None:
        """Ensure doctor_id references a real, active CLINICIAN."""
        doctor = self.user_repository.get_by_id(db, doctor_id)
        if doctor is None or doctor.role != UserRole.CLINICIAN or not doctor.is_active:
            raise EntityNotFoundError("Clinician", doctor_id)

    def _resolve_create_doctor_id(
        self,
        db: Session,
        patient_data: PatientCreate,
        current_user: User,
    ) -> UUID:
        if current_user.role == UserRole.CLINICIAN:
            if patient_data.doctor_id and patient_data.doctor_id != current_user.id:
                raise AuthorizationError(
                    "Clinicians cannot assign patients to another doctor."
                )
            return current_user.id

        # ADMIN path
        if patient_data.doctor_id is None:
            raise ValidationApplicationError(
                "doctor_id is required when creating a patient as admin."
            )
        self._validate_doctor(db, patient_data.doctor_id)
        return patient_data.doctor_id

    def create_patient(
        self,
        db: Session,
        patient_data: PatientCreate,
        current_user: User,
    ) -> Patient:
        """Create a new patient, deriving/validating ownership by role."""

        doctor_id = self._resolve_create_doctor_id(db, patient_data, current_user)
        patient_values = patient_data.model_dump(exclude={"phone", "doctor_id"})
        patient = Patient(
            **patient_values,
            doctor_id=doctor_id,
            phone=[
                PhoneNumber(**phone.model_dump())
                for phone in patient_data.phone
            ],
        )

        return self.repository.create(db, patient)

    def get_patient(
        self,
        db: Session,
        patient_id: UUID,
        current_user: User,
    ) -> Patient:
        """Retrieve a patient by ID, enforcing per-record ownership."""

        patient = self.repository.get_or_404(db, patient_id)
        self._authorize_access(patient, current_user)
        return patient

    def list_patients(
        self,
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        doctor_id: UUID | None = None,
    ) -> tuple[list[Patient], int]:
        """List patients, scoped to the caller's role.

        CLINICIAN always sees only their own patients. ADMIN sees all
        patients, optionally filtered to a single doctor.
        """
        if current_user.role == UserRole.CLINICIAN:
            items = self.repository.get_by_doctor(db, current_user.id, skip, limit)
            total = self.repository.count_by_doctor(db, current_user.id)
            return items, total

        if doctor_id is not None:
            items = self.repository.get_by_doctor(db, doctor_id, skip, limit)
            total = self.repository.count_by_doctor(db, doctor_id)
            return items, total

        items = self.repository.get_all(db, skip, limit)
        total = self.repository.count(db)
        return items, total

    def list_all_patients(self, db: Session, current_user: User) -> list[Patient]:
        """Return every patient the caller may triage, unpaginated.

        Mirrors list_patients' role scoping (CLINICIAN: own patients only;
        ADMIN: everyone), without pagination -- the triage queue (ADR-006)
        must rank the whole panel before paging.
        """
        if current_user.role == UserRole.CLINICIAN:
            return self.repository.get_all_by_doctor(db, current_user.id)
        return self.repository.get_all_active(db)

    def search_patients(
        self,
        db: Session,
        search_term: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Patient], int]:
        """Search patients, scoped to the caller's role."""

        doctor_id = None if current_user.role == UserRole.ADMIN else current_user.id
        items = self.repository.search(
            db, search_term, skip, limit, doctor_id=doctor_id
        )
        total = self.repository.count_search(db, search_term, doctor_id=doctor_id)
        return items, total

    def update_patient(
        self,
        db: Session,
        patient_id: UUID,
        patient_data: PatientUpdate,
        current_user: User,
    ) -> Patient:
        """Update an existing patient, enforcing ownership and doctor_id rules."""

        patient = self.repository.get_or_404(db, patient_id)
        self._authorize_access(patient, current_user)

        if (
            "doctor_id" in patient_data.model_fields_set
            and patient_data.doctor_id is not None
        ):
            if current_user.role == UserRole.CLINICIAN:
                if patient_data.doctor_id != current_user.id:
                    raise AuthorizationError(
                        "Clinicians cannot reassign patients to another doctor."
                    )
            else:
                self._validate_doctor(db, patient_data.doctor_id)
            patient.doctor_id = patient_data.doctor_id

        update_data = patient_data.model_dump(
            exclude_unset=True,
            exclude={"phone", "doctor_id"},
        )

        for field, value in update_data.items():
            setattr(patient, field, value)

        if "phone" in patient_data.model_fields_set:
            patient.phone = [
                PhoneNumber(**phone.model_dump())
                for phone in patient_data.phone or []
            ]

        return self.repository.update(db, patient)

    def delete_patient(
        self,
        db: Session,
        patient_id: UUID,
        current_user: User,
    ) -> None:
        """Soft-delete a patient, enforcing per-record ownership."""

        patient = self.repository.get_or_404(db, patient_id)
        self._authorize_access(patient, current_user)
        self.repository.soft_delete(db, patient)

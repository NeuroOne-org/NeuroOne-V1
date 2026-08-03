"""Business logic for patient management."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Patient
from app.models.patient import PhoneNumber
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate
from app.services.base_service import BaseService


class PatientService(BaseService[PatientRepository]):
    """Business logic for patient management."""

    def __init__(self, repository: PatientRepository):
        super().__init__(repository)

    def create_patient(
        self,
        db: Session,
        patient_data: PatientCreate,
    ) -> Patient:
        """Create a new patient."""

        patient_values = patient_data.model_dump(exclude={"phone"})
        patient = Patient(
            **patient_values,
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
    ) -> Patient | None:
        """Retrieve a patient by ID."""

        return self.repository.get_by_id(db, patient_id)

    def list_patients(self, db: Session) -> list[Patient]:
        """Retrieve all patients."""

        return self.repository.get_all(db)

    def update_patient(
        self,
        db: Session,
        patient_id: UUID,
        patient_data: PatientUpdate,
    ) -> Patient | None:
        """Update an existing patient."""

        patient = self.repository.get_by_id(db, patient_id)

        if patient is None:
            return None

        update_data = patient_data.model_dump(
            exclude_unset=True,
            exclude={"phone"},
        )

        for field, value in update_data.items():
            setattr(patient, field, value)

        if "phone" in patient_data.model_fields_set:
            patient.phone = [
                PhoneNumber(**phone.model_dump())
                for phone in patient_data.phone or []
            ]

        return self.repository.update(db, patient)

    def delete_patient(self, db: Session, patient_id: UUID) -> bool:
        """Soft-delete a patient."""

        patient = self.repository.get_by_id(db, patient_id)

        if patient is None:
            return False

        self.repository.soft_delete(db, patient)

        return True

    def get_patients_by_doctor(
        self,
        db: Session,
        doctor_id: UUID,
    ) -> list[Patient]:
        """Retrieve all patients assigned to a doctor."""

        return self.repository.get_by_doctor(db, doctor_id)

"""Patient persistence operations."""
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Patient
from base_repository import BaseRepository

"""Repository for patient-related database operations.

Provides patient-specific queries and data access methods while
reusing the common CRUD functionality from BaseRepository.
"""


class PatientRepository(BaseRepository[Patient]):
    def __init__(self):
        super().__init__(model=Patient)

    def get_by_doctor(self, db: Session, pid: UUID) -> list[type[Patient]]:
        return db.query(Patient).filter(
            Patient.doctor_id == pid,
            Patient.is_deleted == False,
            ).all()
    def search(self, db: Session) -> list[type[Patient]]:
        pass

    def get_by_phone(self,phone_number:str) -> list[type[Patient]]:
        pass

    def get_by_email(self,email:str) -> list[type[Patient]]:
        pass

    def get_active_patients(self,db: Session) -> list[type[Patient]]:
        pass
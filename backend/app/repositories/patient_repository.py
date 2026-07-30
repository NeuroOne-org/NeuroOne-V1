"""Patient persistence operations."""
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.patient import Patient, PhoneNumber
from app.repositories.base_repository import BaseRepository


class PatientRepository(BaseRepository[Patient]):
    """Provide patient-specific queries in addition to common CRUD operations."""

    def __init__(self):
        super().__init__(model=Patient)

    def get_by_doctor(self, db: Session, pid: UUID) -> list[Patient]:
        return (
            db.query(Patient)
            .filter(
                Patient.doctor_id == pid,
                Patient.is_deleted.is_(False),
            )
            .all()
        )

    def search(
        self,
        db: Session,
        search_term: str = "",
        skip: int = 0,
        limit: int = 100,
    ) -> list[Patient]:
        """Search active patients by name, email, or phone number."""
        term = search_term.strip()
        query = db.query(Patient).filter(Patient.is_deleted.is_(False))

        if term:
            pattern = f"%{term}%"
            query = query.filter(
                or_(
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Patient.email.ilike(pattern),
                    Patient.phone.any(PhoneNumber.phone_number.ilike(pattern)),
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_by_phone(
        self,
        db: Session,
        phone_number: str,
    ) -> Patient | None:
        """Return the active patient with the given phone number, if any."""
        return (
            db.query(Patient)
            .filter(
                Patient.phone.any(PhoneNumber.phone_number == phone_number),
                Patient.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_email(self, db: Session, email: str) -> Patient | None:
        """Return the active patient with the given email address, if any."""
        return (
            db.query(Patient)
            .filter(
                Patient.email == email,
                Patient.is_deleted.is_(False),
            )
            .first()
        )

    def get_active_patients(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Patient]:
        """Return patients that have not been soft-deleted."""
        return (
            db.query(Patient)
            .filter(Patient.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
            .all()
        )

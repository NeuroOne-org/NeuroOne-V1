"""Patient persistence operations."""
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.patient import Patient, PhoneNumber
from app.repositories.base_repository import BaseRepository


class PatientRepository(BaseRepository[Patient]):
    """Provide patient-specific queries in addition to common CRUD operations."""

    def __init__(self):
        super().__init__(model=Patient)

    def get_by_doctor(
        self,
        db: Session,
        pid: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Patient]:
        statement = (
            select(Patient)
            .where(
                Patient.doctor_id == pid,
                Patient.is_deleted.is_(False),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def search(
        self,
        db: Session,
        search_term: str = "",
        skip: int = 0,
        limit: int = 100,
    ) -> list[Patient]:
        """Search active patients by name, email, or phone number."""
        term = search_term.strip()
        statement = select(Patient).where(Patient.is_deleted.is_(False))

        if term:
            pattern = f"%{term}%"
            statement = statement.where(
                or_(
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Patient.email.ilike(pattern),
                    Patient.phone.any(PhoneNumber.phone_number.ilike(pattern)),
                )
            )

        statement = statement.offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    def get_by_phone(
        self,
        db: Session,
        phone_number: str,
    ) -> Patient | None:
        """Return the active patient with the given phone number, if any."""
        statement = select(Patient).where(
            Patient.phone.any(PhoneNumber.phone_number == phone_number),
            Patient.is_deleted.is_(False),
        )
        return db.scalar(statement)

    def get_by_email(self, db: Session, email: str) -> Patient | None:
        """Return the active patient with the given email address, if any."""
        statement = select(Patient).where(
            Patient.email == email,
            Patient.is_deleted.is_(False),
        )
        return db.scalar(statement)

    def get_active_patients(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Patient]:
        """Return patients that have not been soft-deleted."""
        statement = (
            select(Patient)
            .where(Patient.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

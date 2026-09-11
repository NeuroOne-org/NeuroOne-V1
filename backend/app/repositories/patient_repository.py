"""Patient persistence operations."""
from uuid import UUID

from sqlalchemy import func, or_, select
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

    def get_all_by_doctor(self, db: Session, doctor_id: UUID) -> list[Patient]:
        """Return every active patient assigned to a doctor, unpaginated.

        The triage queue (ADR-006) ranks a clinician's whole panel before
        paging, so it needs the full set rather than one page at a time.
        """
        statement = select(Patient).where(
            Patient.doctor_id == doctor_id,
            Patient.is_deleted.is_(False),
        )
        return list(db.scalars(statement).all())

    def get_all_active(self, db: Session) -> list[Patient]:
        """Return every active patient, unpaginated. See get_all_by_doctor."""
        statement = select(Patient).where(Patient.is_deleted.is_(False))
        return list(db.scalars(statement).all())

    def _search_statement(self, search_term: str, doctor_id: UUID | None):
        term = search_term.strip()
        statement = select(Patient).where(Patient.is_deleted.is_(False))

        if doctor_id is not None:
            statement = statement.where(Patient.doctor_id == doctor_id)

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

        return statement

    def search(
        self,
        db: Session,
        search_term: str = "",
        skip: int = 0,
        limit: int = 100,
        doctor_id: UUID | None = None,
    ) -> list[Patient]:
        """Search active patients by name, email, or phone number.

        When ``doctor_id`` is given, results are scoped to that doctor.
        """
        statement = self._search_statement(search_term, doctor_id)
        statement = statement.offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    def count_search(
        self,
        db: Session,
        search_term: str = "",
        doctor_id: UUID | None = None,
    ) -> int:
        """Count patients matching a search, optionally scoped to a doctor."""
        statement = self._search_statement(search_term, doctor_id)
        count_statement = select(func.count()).select_from(statement.subquery())
        return db.scalar(count_statement) or 0

    def count_by_doctor(self, db: Session, doctor_id: UUID) -> int:
        """Count active patients assigned to a doctor."""
        statement = (
            select(func.count())
            .select_from(Patient)
            .where(
                Patient.doctor_id == doctor_id,
                Patient.is_deleted.is_(False),
            )
        )
        return db.scalar(statement) or 0

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

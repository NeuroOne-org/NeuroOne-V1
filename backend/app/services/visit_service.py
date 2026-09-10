"""Business logic for clinical cases (visits) and their symptoms."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.symptom import Symptom
from app.models.user import User
from app.models.visit import Visit, VisitStatus
from app.repositories.symptom_repository import SymptomRepository
from app.repositories.visit_repository import VisitRepository
from app.schemas.symptom import SymptomCreate, SymptomUpdate
from app.schemas.visit import VisitCreate, VisitUpdate
from app.services.base_service import BaseService
from app.services.patient_service import PatientService
from app.utils.exceptions import EntityNotFoundError, ValidationApplicationError


# Written by the AI pipeline (AI-01), never through the visits API.
AI_OWNED_STATUSES = frozenset({VisitStatus.ANALYZED})


class VisitService(BaseService[VisitRepository]):
    """Business logic for clinical cases and symptoms.

    A visit has no doctor_id: ownership is derived from its parent patient, and
    every authorization decision delegates to PatientService so the ADR-001 rule
    lives in exactly one place.
    """

    def __init__(
        self,
        repository: VisitRepository,
        symptom_repository: SymptomRepository,
        patient_service: PatientService,
    ):
        super().__init__(repository)
        self.symptom_repository = symptom_repository
        self.patient_service = patient_service

    def _load_authorized_visit(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
    ) -> Visit:
        """Load a visit the caller may access, or raise a Visit-shaped 404.

        Per ADR-001 all four failure modes are response-identical: the visit is
        missing, the visit is soft-deleted, the parent patient is soft-deleted,
        or the parent patient belongs to another clinician.

        The re-raise matters. PatientService raises EntityNotFoundError with the
        patient id in its message, and on a flat /visits/{id} route the caller
        never supplied that id -- letting it through would leak the parent
        patient UUID to someone with no claim to the record.
        """
        visit = self.repository.get_with_symptoms(db, visit_id)
        if visit is None:
            raise EntityNotFoundError("Visit", visit_id)

        try:
            self.patient_service.get_patient(db, visit.patient_id, current_user)
        except EntityNotFoundError as exc:
            raise EntityNotFoundError("Visit", visit_id) from exc

        return visit

    def _load_authorized_symptom(
        self,
        db: Session,
        visit_id: UUID,
        symptom_id: UUID,
        current_user: User,
    ) -> Symptom:
        """Load a symptom on an accessible visit, or raise a 404.

        The visit_id check closes the mismatched-pair hole: a symptom belonging
        to another visit reads as absent rather than being silently edited.
        """
        visit = self._load_authorized_visit(db, visit_id, current_user)

        symptom = self.symptom_repository.get_by_id(db, symptom_id)
        if symptom is None or symptom.visit_id != visit.id:
            raise EntityNotFoundError("Symptom", symptom_id)

        return symptom

    def _reject_ai_owned_status(self, status: VisitStatus | None) -> None:
        """Reject statuses only the AI pipeline may write."""
        if status is not None and status in AI_OWNED_STATUSES:
            raise ValidationApplicationError(
                f"Status '{status.value}' is set by the analysis pipeline "
                "and cannot be assigned through the visits API."
            )

    def create_visit(
        self,
        db: Session,
        patient_id: UUID,
        visit_data: VisitCreate,
        current_user: User,
    ) -> Visit:
        """Open a clinical case for a patient the caller owns.

        The patient id came from the path, so an ownership failure keeps its
        honest "Patient not found" label here.
        """
        self.patient_service.get_patient(db, patient_id, current_user)
        self._reject_ai_owned_status(visit_data.status)

        # Symptoms are attached before create() so the delete-orphan cascade
        # inserts the whole case in one commit -- a failure rolls back the
        # visit and its symptoms together.
        visit = Visit(
            patient_id=patient_id,
            visit_date=visit_data.visit_date or datetime.now(timezone.utc),
            chief_complaint=visit_data.chief_complaint,
            history=visit_data.history,
            vitals=visit_data.vitals.model_dump(exclude_none=True),
            notes=visit_data.notes,
            status=visit_data.status or VisitStatus.DRAFT,
            symptoms=[
                Symptom(**symptom.model_dump()) for symptom in visit_data.symptoms
            ],
        )

        return self.repository.create(db, visit)

    def get_visit(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
    ) -> Visit:
        """Retrieve a visit by ID. Ownership violations read as 404."""

        return self._load_authorized_visit(db, visit_id, current_user)

    def list_patient_visits(
        self,
        db: Session,
        patient_id: UUID,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        status: VisitStatus | None = None,
    ) -> tuple[list[Visit], int]:
        """List a patient's visits, newest first."""

        self.patient_service.get_patient(db, patient_id, current_user)
        items = self.repository.get_by_patient(db, patient_id, skip, limit, status)
        total = self.repository.count_by_patient(db, patient_id, status)
        return items, total

    def get_patient_history(
        self,
        db: Session,
        patient_id: UUID,
        current_user: User,
        *,
        limit: int = 10,
        newest_first: bool = True,
        exclude_visit_id: UUID | None = None,
    ) -> tuple[list[Visit], int]:
        """Return a patient's visit history ordered for trend comparison.

        This is the in-process entry point the AI context builder (AI-01) calls;
        it must not go through the HTTP endpoint. CASE-01 returns raw ordered
        history and computes no trends -- interpretation is the AI layer's job.
        """
        self.patient_service.get_patient(db, patient_id, current_user)

        visits = self.repository.get_history(
            db,
            patient_id,
            limit=limit,
            newest_first=newest_first,
            exclude_visit_id=exclude_visit_id,
        )
        total = self.repository.count_by_patient(db, patient_id)
        return visits, total

    def update_visit(
        self,
        db: Session,
        visit_id: UUID,
        visit_data: VisitUpdate,
        current_user: User,
    ) -> Visit:
        """Partially update a visit. Ownership violations read as 404."""

        visit = self._load_authorized_visit(db, visit_id, current_user)
        self._reject_ai_owned_status(visit_data.status)

        update_data = visit_data.model_dump(exclude_unset=True, exclude={"vitals"})
        for field, value in update_data.items():
            setattr(visit, field, value)

        if "vitals" in visit_data.model_fields_set and visit_data.vitals is not None:
            visit.vitals = visit_data.vitals.model_dump(exclude_none=True)

        return self.repository.update(db, visit)

    def delete_visit(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
    ) -> None:
        """Soft-delete a visit and its symptoms."""

        visit = self._load_authorized_visit(db, visit_id, current_user)

        for symptom in visit.symptoms:
            if not symptom.is_deleted:
                symptom.soft_delete()

        self.repository.soft_delete(db, visit)

    def list_symptoms(
        self,
        db: Session,
        visit_id: UUID,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Symptom], int]:
        """List a visit's symptoms in recording order."""

        self._load_authorized_visit(db, visit_id, current_user)
        items = self.symptom_repository.get_by_visit(db, visit_id, skip, limit)
        total = self.symptom_repository.count_by_visit(db, visit_id)
        return items, total

    def add_symptom(
        self,
        db: Session,
        visit_id: UUID,
        symptom_data: SymptomCreate,
        current_user: User,
    ) -> Symptom:
        """Record a symptom against a visit."""

        visit = self._load_authorized_visit(db, visit_id, current_user)
        symptom = Symptom(visit_id=visit.id, **symptom_data.model_dump())
        return self.symptom_repository.create(db, symptom)

    def update_symptom(
        self,
        db: Session,
        visit_id: UUID,
        symptom_id: UUID,
        symptom_data: SymptomUpdate,
        current_user: User,
    ) -> Symptom:
        """Partially update a symptom on a visit."""

        symptom = self._load_authorized_symptom(
            db, visit_id, symptom_id, current_user
        )

        update_data = symptom_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(symptom, field, value)

        return self.symptom_repository.update(db, symptom)

    def delete_symptom(
        self,
        db: Session,
        visit_id: UUID,
        symptom_id: UUID,
        current_user: User,
    ) -> None:
        """Soft-delete a symptom on a visit."""

        symptom = self._load_authorized_symptom(
            db, visit_id, symptom_id, current_user
        )
        self.symptom_repository.soft_delete(db, symptom)

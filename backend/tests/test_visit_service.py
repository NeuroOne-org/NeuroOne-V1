"""Unit tests for VisitService ownership derivation and 404 masking.

The load-bearing property here is that ownership is derived from the parent
patient without ever disclosing that patient. See ADR-002.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.models.symptom import Symptom
from app.models.user import User, UserRole
from app.models.visit import Visit, VisitStatus
from app.schemas.symptom import SymptomCreate, SymptomUpdate
from app.schemas.visit import VisitCreate, VisitUpdate, Vitals
from app.services.visit_service import VisitService
from app.utils.exceptions import EntityNotFoundError, ValidationApplicationError


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


def _user(role: UserRole = UserRole.CLINICIAN) -> User:
    return User(
        id=uuid4(),
        username=f"user-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hash",
        role=role,
        is_active=True,
        is_verified=True,
        is_deleted=False,
    )


def _visit(patient_id=None, *, symptoms=()) -> Visit:
    return Visit(
        id=uuid4(),
        patient_id=patient_id or uuid4(),
        visit_date=NOW,
        chief_complaint="tremor",
        vitals={},
        status=VisitStatus.DRAFT,
        symptoms=list(symptoms),
    )


def _symptom(visit_id=None, *, name="tremor", severity=5) -> Symptom:
    return Symptom(
        id=uuid4(),
        visit_id=visit_id or uuid4(),
        symptom_name=name,
        severity=severity,
    )


def _create_payload(**overrides) -> VisitCreate:
    payload = {
        "chief_complaint": "progressive tremor",
        "history": "six months",
        "vitals": Vitals(heart_rate=72),
        "symptoms": [],
    }
    payload.update(overrides)
    return VisitCreate(**payload)


def _service() -> tuple[VisitService, Mock, Mock, Mock]:
    repository = Mock()
    symptom_repository = Mock()
    patient_service = Mock()
    service = VisitService(repository, symptom_repository, patient_service)
    return service, repository, symptom_repository, patient_service


def _deny_patient(patient_service: Mock) -> None:
    """Make the patient gate behave as it does for a non-owned patient."""
    patient_service.get_patient.side_effect = EntityNotFoundError("Patient", uuid4())


# --------------------------------------------------------------------------
# Ownership derivation and masking
# --------------------------------------------------------------------------


def test_visit_on_another_clinicians_patient_reads_as_a_missing_visit() -> None:
    service, repository, _, patient_service = _service()
    visit = _visit()
    repository.get_with_symptoms.return_value = visit
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_visit(Mock(), visit.id, _user())

    assert exc_info.value.entity == "Visit"
    assert exc_info.value.identifier == visit.id
    # The parent patient must not leak through the masked error.
    assert str(visit.patient_id) not in exc_info.value.message


def test_missing_visit_and_unauthorized_visit_raise_the_same_shape() -> None:
    service, repository, _, patient_service = _service()
    unauthorized = _visit()
    absent_id = uuid4()

    repository.get_with_symptoms.return_value = unauthorized
    _deny_patient(patient_service)
    with pytest.raises(EntityNotFoundError) as denied:
        service.get_visit(Mock(), unauthorized.id, _user())

    repository.get_with_symptoms.return_value = None
    with pytest.raises(EntityNotFoundError) as missing:
        service.get_visit(Mock(), absent_id, _user())

    assert denied.value.entity == missing.value.entity == "Visit"
    assert denied.value.error_code == missing.value.error_code
    assert denied.value.message.replace(
        str(unauthorized.id), ""
    ) == missing.value.message.replace(str(absent_id), "")


def test_soft_deleted_visit_reads_as_missing() -> None:
    service, repository, _, _ = _service()
    repository.get_with_symptoms.return_value = None

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_visit(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Visit"


def test_admin_reaches_any_visit() -> None:
    service, repository, _, patient_service = _service()
    visit = _visit()
    repository.get_with_symptoms.return_value = visit

    assert service.get_visit(Mock(), visit.id, _user(UserRole.ADMIN)) is visit
    patient_service.get_patient.assert_called_once()


def test_owned_visit_is_returned_with_its_symptoms() -> None:
    service, repository, _, _ = _service()
    visit = _visit(symptoms=[_symptom()])
    repository.get_with_symptoms.return_value = visit

    result = service.get_visit(Mock(), visit.id, _user())

    assert result is visit
    assert len(result.symptoms) == 1


# --------------------------------------------------------------------------
# Create
# --------------------------------------------------------------------------


def test_create_on_another_doctors_patient_names_the_patient() -> None:
    """The path supplied the patient id, so the honest label is correct here."""
    service, repository, _, patient_service = _service()
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.create_visit(Mock(), uuid4(), _create_payload(), _user())

    assert exc_info.value.entity == "Patient"
    repository.create.assert_not_called()


def test_create_defaults_to_draft_and_now() -> None:
    service, repository, _, _ = _service()
    repository.create.side_effect = lambda db, obj: obj
    patient_id = uuid4()

    before = datetime.now(timezone.utc)
    visit = service.create_visit(Mock(), patient_id, _create_payload(), _user())

    assert visit.patient_id == patient_id
    assert visit.status == VisitStatus.DRAFT
    assert before <= visit.visit_date <= datetime.now(timezone.utc)
    assert visit.vitals == {"heart_rate": 72}


def test_create_attaches_nested_symptoms_before_persisting() -> None:
    service, repository, _, _ = _service()
    repository.create.side_effect = lambda db, obj: obj

    visit = service.create_visit(
        Mock(),
        uuid4(),
        _create_payload(
            symptoms=[
                SymptomCreate(symptom_name="tremor", severity=4, onset="gradual"),
                SymptomCreate(symptom_name="aphasia", severity=6),
            ]
        ),
        _user(),
    )

    # One create call: the cascade inserts the case and its symptoms together.
    repository.create.assert_called_once()
    persisted = repository.create.call_args.args[1]
    assert [symptom.symptom_name for symptom in persisted.symptoms] == [
        "tremor",
        "aphasia",
    ]
    assert visit.symptoms[0].onset == "gradual"


def test_create_honours_an_explicit_visit_date() -> None:
    service, repository, _, _ = _service()
    repository.create.side_effect = lambda db, obj: obj
    backdated = NOW - timedelta(days=90)

    visit = service.create_visit(
        Mock(), uuid4(), _create_payload(visit_date=backdated), _user()
    )

    assert visit.visit_date == backdated


def test_create_rejects_the_ai_owned_status() -> None:
    service, repository, _, _ = _service()

    with pytest.raises(ValidationApplicationError):
        service.create_visit(
            Mock(),
            uuid4(),
            _create_payload(status=VisitStatus.ANALYZED),
            _user(),
        )

    repository.create.assert_not_called()


def test_create_allows_submitting_a_case() -> None:
    service, repository, _, _ = _service()
    repository.create.side_effect = lambda db, obj: obj

    visit = service.create_visit(
        Mock(), uuid4(), _create_payload(status=VisitStatus.SUBMITTED), _user()
    )

    assert visit.status == VisitStatus.SUBMITTED


# --------------------------------------------------------------------------
# Update and delete
# --------------------------------------------------------------------------


def test_update_leaves_unset_fields_untouched() -> None:
    service, repository, _, _ = _service()
    visit = _visit()
    visit.history = "original"
    repository.get_with_symptoms.return_value = visit
    repository.update.side_effect = lambda db, obj: obj

    result = service.update_visit(
        Mock(), visit.id, VisitUpdate(chief_complaint="worsening tremor"), _user()
    )

    assert result.chief_complaint == "worsening tremor"
    assert result.history == "original"


def test_update_applies_an_explicit_null() -> None:
    service, repository, _, _ = _service()
    visit = _visit()
    visit.notes = "original"
    repository.get_with_symptoms.return_value = visit
    repository.update.side_effect = lambda db, obj: obj

    result = service.update_visit(Mock(), visit.id, VisitUpdate(notes=None), _user())

    assert result.notes is None


def test_update_replaces_vitals_wholesale() -> None:
    service, repository, _, _ = _service()
    visit = _visit()
    visit.vitals = {"heart_rate": 60, "spo2": 98}
    repository.get_with_symptoms.return_value = visit
    repository.update.side_effect = lambda db, obj: obj

    result = service.update_visit(
        Mock(), visit.id, VisitUpdate(vitals=Vitals(heart_rate=88)), _user()
    )

    assert result.vitals == {"heart_rate": 88}


def test_update_rejects_the_ai_owned_status() -> None:
    service, repository, _, _ = _service()
    repository.get_with_symptoms.return_value = _visit()

    with pytest.raises(ValidationApplicationError):
        service.update_visit(
            Mock(), uuid4(), VisitUpdate(status=VisitStatus.ANALYZED), _user()
        )

    repository.update.assert_not_called()


def test_update_on_a_non_owned_visit_never_reaches_the_repository() -> None:
    service, repository, _, patient_service = _service()
    repository.get_with_symptoms.return_value = _visit()
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.update_visit(
            Mock(), uuid4(), VisitUpdate(chief_complaint="edited"), _user()
        )

    assert exc_info.value.entity == "Visit"
    repository.update.assert_not_called()


def test_delete_soft_deletes_the_visit_and_its_live_symptoms() -> None:
    service, repository, _, _ = _service()
    live = _symptom(name="live")
    already_gone = _symptom(name="already-gone")
    already_gone.soft_delete()
    original_deleted_at = already_gone.deleted_at

    visit = _visit(symptoms=[live, already_gone])
    repository.get_with_symptoms.return_value = visit

    service.delete_visit(Mock(), visit.id, _user())

    assert live.is_deleted
    assert already_gone.deleted_at == original_deleted_at
    repository.soft_delete.assert_called_once()
    assert repository.soft_delete.call_args.args[1] is visit


def test_delete_on_a_non_owned_visit_never_reaches_the_repository() -> None:
    service, repository, _, patient_service = _service()
    visit = _visit(symptoms=[_symptom()])
    repository.get_with_symptoms.return_value = visit
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.delete_visit(Mock(), visit.id, _user())

    assert exc_info.value.entity == "Visit"
    repository.soft_delete.assert_not_called()
    assert not visit.symptoms[0].is_deleted


# --------------------------------------------------------------------------
# Symptoms
# --------------------------------------------------------------------------


def test_symptom_from_another_visit_reads_as_a_missing_symptom() -> None:
    service, repository, symptom_repository, _ = _service()
    visit = _visit()
    repository.get_with_symptoms.return_value = visit
    symptom_repository.get_by_id.return_value = _symptom(visit_id=uuid4())

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.update_symptom(
            Mock(), visit.id, uuid4(), SymptomUpdate(severity=9), _user()
        )

    assert exc_info.value.entity == "Symptom"
    symptom_repository.update.assert_not_called()


def test_symptom_on_another_clinicians_visit_reads_as_a_missing_visit() -> None:
    """Masking survives one level of nesting: the visit, not the symptom, 404s."""
    service, repository, symptom_repository, patient_service = _service()
    visit = _visit()
    repository.get_with_symptoms.return_value = visit
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.delete_symptom(Mock(), visit.id, uuid4(), _user())

    assert exc_info.value.entity == "Visit"
    assert str(visit.patient_id) not in exc_info.value.message
    symptom_repository.get_by_id.assert_not_called()
    symptom_repository.soft_delete.assert_not_called()


def test_add_symptom_binds_it_to_the_authorized_visit() -> None:
    service, repository, symptom_repository, _ = _service()
    visit = _visit()
    repository.get_with_symptoms.return_value = visit
    symptom_repository.create.side_effect = lambda db, obj: obj

    symptom = service.add_symptom(
        Mock(),
        visit.id,
        SymptomCreate(symptom_name="ataxia", severity=7, duration_days=30),
        _user(),
    )

    assert symptom.visit_id == visit.id
    assert symptom.symptom_name == "ataxia"
    assert symptom.duration_days == 30


def test_add_symptom_persists_a_clinician_observation() -> None:
    """FR-03: observation is a structured field, distinct from severity/onset."""
    service, repository, symptom_repository, _ = _service()
    visit = _visit()
    repository.get_with_symptoms.return_value = visit
    symptom_repository.create.side_effect = lambda db, obj: obj

    symptom = service.add_symptom(
        Mock(),
        visit.id,
        SymptomCreate(
            symptom_name="tremor",
            severity=5,
            observation="worse with intention, resolves at rest",
        ),
        _user(),
    )

    assert symptom.observation == "worse with intention, resolves at rest"


def test_add_symptom_on_a_non_owned_visit_is_refused() -> None:
    service, repository, symptom_repository, patient_service = _service()
    repository.get_with_symptoms.return_value = _visit()
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.add_symptom(
            Mock(), uuid4(), SymptomCreate(symptom_name="ataxia", severity=7), _user()
        )

    assert exc_info.value.entity == "Visit"
    symptom_repository.create.assert_not_called()


def test_update_symptom_applies_only_the_set_fields() -> None:
    service, repository, symptom_repository, _ = _service()
    visit = _visit()
    symptom = _symptom(visit_id=visit.id, name="tremor", severity=3)
    repository.get_with_symptoms.return_value = visit
    symptom_repository.get_by_id.return_value = symptom
    symptom_repository.update.side_effect = lambda db, obj: obj

    result = service.update_symptom(
        Mock(), visit.id, symptom.id, SymptomUpdate(severity=8), _user()
    )

    assert result.severity == 8
    assert result.symptom_name == "tremor"


def test_update_symptom_can_set_the_observation() -> None:
    service, repository, symptom_repository, _ = _service()
    visit = _visit()
    symptom = _symptom(visit_id=visit.id, name="tremor", severity=3)
    repository.get_with_symptoms.return_value = visit
    symptom_repository.get_by_id.return_value = symptom
    symptom_repository.update.side_effect = lambda db, obj: obj

    result = service.update_symptom(
        Mock(),
        visit.id,
        symptom.id,
        SymptomUpdate(observation="new onset since last visit"),
        _user(),
    )

    assert result.observation == "new onset since last visit"


# --------------------------------------------------------------------------
# History
# --------------------------------------------------------------------------


def test_history_passes_its_window_through_to_the_repository() -> None:
    service, repository, _, _ = _service()
    patient_id, current_visit_id = uuid4(), uuid4()
    repository.get_history.return_value = [_visit(patient_id)]
    repository.count_by_patient.return_value = 7

    visits, total = service.get_patient_history(
        Mock(),
        patient_id,
        _user(),
        limit=3,
        newest_first=False,
        exclude_visit_id=current_visit_id,
    )

    assert total == 7
    assert len(visits) == 1
    kwargs = repository.get_history.call_args.kwargs
    assert kwargs["limit"] == 3
    assert kwargs["newest_first"] is False
    assert kwargs["exclude_visit_id"] == current_visit_id


def test_history_for_another_doctors_patient_is_refused_before_any_query() -> None:
    service, repository, _, patient_service = _service()
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.get_patient_history(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Patient"
    repository.get_history.assert_not_called()


def test_listing_visits_is_scoped_to_the_authorized_patient() -> None:
    service, repository, _, patient_service = _service()
    patient_id = uuid4()
    repository.get_by_patient.return_value = [_visit(patient_id)]
    repository.count_by_patient.return_value = 1

    items, total = service.list_patient_visits(Mock(), patient_id, _user())

    assert total == 1
    assert items[0].patient_id == patient_id
    patient_service.get_patient.assert_called_once()


def test_listing_visits_for_another_doctors_patient_is_refused() -> None:
    service, repository, _, patient_service = _service()
    _deny_patient(patient_service)

    with pytest.raises(EntityNotFoundError) as exc_info:
        service.list_patient_visits(Mock(), uuid4(), _user())

    assert exc_info.value.entity == "Patient"
    repository.get_by_patient.assert_not_called()

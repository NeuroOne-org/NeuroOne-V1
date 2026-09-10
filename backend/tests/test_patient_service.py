"""Unit tests for PatientService ownership and doctor_id resolution rules."""

from datetime import date
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.models.patient import Patient
from app.models.user import User, UserRole
from app.schemas.patient import PatientCreate, PatientUpdate, PhoneNumber
from app.services.patient_service import PatientService
from app.utils.exceptions import (
    AuthorizationError,
    EntityNotFoundError,
    ValidationApplicationError,
)


def _user(role: UserRole = UserRole.CLINICIAN, *, is_active: bool = True) -> User:
    return User(
        id=uuid4(),
        username=f"user-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hash",
        role=role,
        is_active=is_active,
        is_verified=True,
        is_deleted=False,
    )


def _patient(doctor_id) -> Patient:
    return Patient(
        id=uuid4(),
        doctor_id=doctor_id,
        first_name="Pat",
        last_name="Ient",
        gender="F",
        dob=date(1990, 1, 1),
        email=f"{uuid4().hex[:8]}@example.com",
        address="123 Main St",
        blood_group="O+",
        allergies=[],
        emergency_contact="1234567890",
    )


def _create_payload(doctor_id=None) -> PatientCreate:
    return PatientCreate(
        first_name="Pat",
        last_name="Ient",
        gender="F",
        dob=date(1990, 1, 1),
        phone=[PhoneNumber(phone_number="1234567890")],
        email=f"{uuid4().hex[:8]}@example.com",
        address="123 Main St",
        blood_group="O+",
        allergies=[],
        emergency_contact="1234567890",
        doctor_id=doctor_id,
    )


def _service() -> tuple[PatientService, Mock, Mock]:
    repository = Mock()
    user_repository = Mock()
    return PatientService(repository, user_repository), repository, user_repository


# --- _authorize_access -------------------------------------------------


def test_admin_may_access_any_patient() -> None:
    service, _, _ = _service()
    admin = _user(UserRole.ADMIN)
    patient = _patient(doctor_id=uuid4())

    service._authorize_access(patient, admin)  # no raise


def test_clinician_may_access_own_patient() -> None:
    service, _, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    patient = _patient(doctor_id=clinician.id)

    service._authorize_access(patient, clinician)  # no raise


def test_clinician_accessing_other_doctors_patient_gets_not_found() -> None:
    service, _, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    patient = _patient(doctor_id=uuid4())

    with pytest.raises(EntityNotFoundError):
        service._authorize_access(patient, clinician)


# --- create_patient / doctor_id resolution ------------------------------


def test_clinician_create_defaults_doctor_id_to_self() -> None:
    service, repository, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    repository.create.side_effect = lambda db, patient: patient

    patient = service.create_patient(db=Mock(), patient_data=_create_payload(), current_user=clinician)

    assert patient.doctor_id == clinician.id


def test_clinician_create_cannot_assign_another_doctor() -> None:
    service, _, _ = _service()
    clinician = _user(UserRole.CLINICIAN)

    with pytest.raises(AuthorizationError):
        service.create_patient(
            db=Mock(),
            patient_data=_create_payload(doctor_id=uuid4()),
            current_user=clinician,
        )


def test_admin_create_requires_doctor_id() -> None:
    service, _, _ = _service()
    admin = _user(UserRole.ADMIN)

    with pytest.raises(ValidationApplicationError):
        service.create_patient(
            db=Mock(), patient_data=_create_payload(), current_user=admin
        )


def test_admin_create_rejects_unknown_doctor() -> None:
    service, _, user_repository = _service()
    admin = _user(UserRole.ADMIN)
    user_repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.create_patient(
            db=Mock(),
            patient_data=_create_payload(doctor_id=uuid4()),
            current_user=admin,
        )


def test_admin_create_rejects_non_clinician_doctor() -> None:
    service, _, user_repository = _service()
    admin = _user(UserRole.ADMIN)
    user_repository.get_by_id.return_value = _user(UserRole.ADMIN)

    with pytest.raises(EntityNotFoundError):
        service.create_patient(
            db=Mock(),
            patient_data=_create_payload(doctor_id=uuid4()),
            current_user=admin,
        )


def test_admin_create_accepts_valid_clinician_doctor() -> None:
    service, repository, user_repository = _service()
    admin = _user(UserRole.ADMIN)
    target_doctor = _user(UserRole.CLINICIAN)
    user_repository.get_by_id.return_value = target_doctor
    repository.create.side_effect = lambda db, patient: patient

    patient = service.create_patient(
        db=Mock(),
        patient_data=_create_payload(doctor_id=target_doctor.id),
        current_user=admin,
    )

    assert patient.doctor_id == target_doctor.id


# --- get_patient ---------------------------------------------------------


def test_get_patient_hides_ownership_violation_as_not_found() -> None:
    service, repository, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    repository.get_or_404.return_value = _patient(doctor_id=uuid4())

    with pytest.raises(EntityNotFoundError):
        service.get_patient(db=Mock(), patient_id=uuid4(), current_user=clinician)


# --- update_patient --------------------------------------------------------


def test_clinician_cannot_reassign_patient_on_update() -> None:
    service, repository, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    patient = _patient(doctor_id=clinician.id)
    repository.get_or_404.return_value = patient

    with pytest.raises(AuthorizationError):
        service.update_patient(
            db=Mock(),
            patient_id=patient.id,
            patient_data=PatientUpdate(doctor_id=uuid4()),
            current_user=clinician,
        )


def test_admin_update_rejects_invalid_reassignment() -> None:
    service, repository, user_repository = _service()
    admin = _user(UserRole.ADMIN)
    patient = _patient(doctor_id=uuid4())
    repository.get_or_404.return_value = patient
    user_repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.update_patient(
            db=Mock(),
            patient_id=patient.id,
            patient_data=PatientUpdate(doctor_id=uuid4()),
            current_user=admin,
        )


def test_update_on_other_doctors_patient_is_not_found() -> None:
    service, repository, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    patient = _patient(doctor_id=uuid4())
    repository.get_or_404.return_value = patient

    with pytest.raises(EntityNotFoundError):
        service.update_patient(
            db=Mock(),
            patient_id=patient.id,
            patient_data=PatientUpdate(first_name="New"),
            current_user=clinician,
        )


# --- delete_patient --------------------------------------------------------


def test_delete_on_other_doctors_patient_is_not_found() -> None:
    service, repository, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    patient = _patient(doctor_id=uuid4())
    repository.get_or_404.return_value = patient

    with pytest.raises(EntityNotFoundError):
        service.delete_patient(db=Mock(), patient_id=patient.id, current_user=clinician)

    repository.soft_delete.assert_not_called()


def test_delete_own_patient_succeeds() -> None:
    service, repository, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    patient = _patient(doctor_id=clinician.id)
    repository.get_or_404.return_value = patient

    service.delete_patient(db=Mock(), patient_id=patient.id, current_user=clinician)

    repository.soft_delete.assert_called_once()


# --- list_patients / search_patients scoping --------------------------------


def test_clinician_list_is_scoped_to_own_patients() -> None:
    service, repository, _ = _service()
    clinician = _user(UserRole.CLINICIAN)
    repository.get_by_doctor.return_value = []
    repository.count_by_doctor.return_value = 0

    service.list_patients(db=Mock(), current_user=clinician)

    repository.get_by_doctor.assert_called_once()
    repository.get_all.assert_not_called()


def test_admin_list_without_filter_sees_everyone() -> None:
    service, repository, _ = _service()
    admin = _user(UserRole.ADMIN)
    repository.get_all.return_value = []
    repository.count.return_value = 0

    service.list_patients(db=Mock(), current_user=admin)

    repository.get_all.assert_called_once()
    repository.get_by_doctor.assert_not_called()


def test_admin_search_is_unscoped_clinician_search_is_scoped() -> None:
    service, repository, _ = _service()
    admin = _user(UserRole.ADMIN)
    clinician = _user(UserRole.CLINICIAN)
    repository.search.return_value = []
    repository.count_search.return_value = 0

    service.search_patients(db=Mock(), search_term="x", current_user=admin)
    assert repository.search.call_args.kwargs["doctor_id"] is None

    service.search_patients(db=Mock(), search_term="x", current_user=clinician)
    assert repository.search.call_args.kwargs["doctor_id"] == clinician.id

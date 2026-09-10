"""Integration-style contract tests for patient endpoints.

Covers the ownership-enforcement surface introduced by PAT-01: CLINICIAN
self-scoping, ADMIN full access, and ADR-001's requirement that ownership
violations be response-indistinguishable from a genuinely missing record.
"""

from datetime import date, datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies import get_current_active_user, get_db, get_patient_service
from app.models.patient import Patient, PhoneNumber
from app.models.user import User, UserRole
from app.utils.exceptions import AuthorizationError, EntityNotFoundError
from main import app


def _user(role: UserRole = UserRole.CLINICIAN) -> User:
    now = datetime.now(timezone.utc)
    return User(
        id=uuid4(),
        username=f"user-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="not-returned",
        role=role,
        is_active=True,
        is_verified=True,
        is_deleted=False,
        created_at=now,
        updated_at=now,
    )


def _patient(doctor: User) -> Patient:
    now = datetime.now(timezone.utc)
    patient = Patient(
        id=uuid4(),
        doctor_id=doctor.id,
        first_name="Pat",
        last_name="Ient",
        gender="F",
        dob=date(1990, 1, 1),
        email=f"{uuid4().hex[:8]}@example.com",
        address="123 Main St",
        blood_group="O+",
        allergies=[],
        emergency_contact="1234567890",
        created_at=now,
        updated_at=now,
    )
    patient.phone = [PhoneNumber(patient_id=patient.id, phone_number="1234567890")]
    patient.doctor = doctor
    return patient


def _db_override():
    yield object()


def _client(current_user: User, service_stub) -> TestClient:
    app.dependency_overrides[get_db] = _db_override
    app.dependency_overrides[get_current_active_user] = lambda: current_user
    app.dependency_overrides[get_patient_service] = lambda: service_stub
    return TestClient(app, raise_server_exceptions=False)


def teardown_function() -> None:
    app.dependency_overrides.clear()


def test_clinician_cannot_create_patient_for_another_doctor() -> None:
    clinician = _user(UserRole.CLINICIAN)

    class ServiceStub:
        def create_patient(self, db, patient_data, current_user):
            raise AuthorizationError(
                "Clinicians cannot assign patients to another doctor."
            )

    client = _client(clinician, ServiceStub())
    response = client.post(
        "/api/v1/patients",
        json={
            "first_name": "Pat",
            "gender": "F",
            "dob": "1990-01-01",
            "phone": [{"phone_number": "1234567890"}],
            "email": "pat@example.com",
            "address": "123 Main St",
            "blood_group": "O+",
            "allergies": [],
            "emergency_contact": "1234567890",
            "doctor_id": str(uuid4()),
        },
    )

    assert response.status_code == 403
    assert response.json()["error_code"] == "authorization_error"


def test_get_own_patient_succeeds() -> None:
    clinician = _user(UserRole.CLINICIAN)
    patient = _patient(clinician)

    class ServiceStub:
        def get_patient(self, db, patient_id, current_user):
            assert current_user is clinician
            return patient

    client = _client(clinician, ServiceStub())
    response = client.get(f"/api/v1/patients/{patient.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(patient.id)


def test_ownership_violation_and_true_absence_return_identical_404() -> None:
    clinician = _user(UserRole.CLINICIAN)

    class NotFoundServiceStub:
        def get_patient(self, db, patient_id, current_user):
            raise EntityNotFoundError("Patient", patient_id)

    other_patient_id = uuid4()
    nonexistent_id = uuid4()

    client = _client(clinician, NotFoundServiceStub())
    owned_by_other = client.get(f"/api/v1/patients/{other_patient_id}")
    truly_missing = client.get(f"/api/v1/patients/{nonexistent_id}")

    assert owned_by_other.status_code == 404
    assert truly_missing.status_code == 404
    assert owned_by_other.json()["error_code"] == truly_missing.json()["error_code"]
    assert set(owned_by_other.json().keys()) == set(truly_missing.json().keys())


def test_update_on_other_doctors_patient_is_404() -> None:
    clinician = _user(UserRole.CLINICIAN)

    class ServiceStub:
        def update_patient(self, db, patient_id, patient_data, current_user):
            raise EntityNotFoundError("Patient", patient_id)

    client = _client(clinician, ServiceStub())
    response = client.patch(
        f"/api/v1/patients/{uuid4()}",
        json={"first_name": "Changed"},
    )

    assert response.status_code == 404


def test_delete_on_other_doctors_patient_is_404() -> None:
    clinician = _user(UserRole.CLINICIAN)

    class ServiceStub:
        def delete_patient(self, db, patient_id, current_user):
            raise EntityNotFoundError("Patient", patient_id)

    client = _client(clinician, ServiceStub())
    response = client.delete(f"/api/v1/patients/{uuid4()}")

    assert response.status_code == 404


def test_delete_own_patient_returns_204() -> None:
    clinician = _user(UserRole.CLINICIAN)

    class ServiceStub:
        def delete_patient(self, db, patient_id, current_user):
            return None

    client = _client(clinician, ServiceStub())
    response = client.delete(f"/api/v1/patients/{uuid4()}")

    assert response.status_code == 204


def test_list_patients_returns_page_based_pagination_shape() -> None:
    admin = _user(UserRole.ADMIN)
    patient = _patient(_user(UserRole.CLINICIAN))

    class ServiceStub:
        def list_patients(self, db, current_user, skip, limit, doctor_id):
            return [patient], 1

    client = _client(admin, ServiceStub())
    response = client.get("/api/v1/patients")

    assert response.status_code == 200
    body = response.json()
    assert body["pagination"] == {
        "page": 1,
        "page_size": 20,
        "total_records": 1,
        "total_pages": 1,
    }
    assert len(body["items"]) == 1


def test_search_route_is_reachable_and_not_shadowed_by_id_route() -> None:
    admin = _user(UserRole.ADMIN)

    class ServiceStub:
        def search_patients(self, db, search_term, current_user, skip, limit):
            assert search_term == "smith"
            return [], 0

    client = _client(admin, ServiceStub())
    response = client.get("/api/v1/patients/search", params={"q": "smith"})

    assert response.status_code == 200
    assert response.json()["items"] == []

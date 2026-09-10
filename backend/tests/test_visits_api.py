"""Contract tests for the clinical case (visit) and symptom endpoints.

Extends PAT-01's ADR-001 parity requirement one level down: a visit on another
clinician's patient must be response-indistinguishable from a missing visit,
and must not disclose the parent patient. See ADR-002.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies import get_current_active_user, get_db, get_visit_service
from app.models.symptom import Symptom
from app.models.user import User, UserRole
from app.models.visit import Visit, VisitStatus
from app.utils.exceptions import EntityNotFoundError, ValidationApplicationError
from main import app


NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)


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


def _symptom(visit_id, *, name="tremor", severity=5) -> Symptom:
    now = datetime.now(timezone.utc)
    return Symptom(
        id=uuid4(),
        visit_id=visit_id,
        symptom_name=name,
        severity=severity,
        duration_days=30,
        onset="gradual",
        created_at=now,
        updated_at=now,
    )


def _visit(patient_id=None, *, days_offset=0, symptom_names=("tremor",)) -> Visit:
    now = datetime.now(timezone.utc)
    visit_id = uuid4()
    visit = Visit(
        id=visit_id,
        patient_id=patient_id or uuid4(),
        visit_date=NOW + timedelta(days=days_offset),
        chief_complaint="progressive tremor",
        history="six months",
        vitals={"heart_rate": 72},
        notes=None,
        status=VisitStatus.DRAFT,
        created_at=now,
        updated_at=now,
    )
    visit.symptoms = [_symptom(visit_id, name=name) for name in symptom_names]
    return visit


def _db_override():
    yield object()


def _client(current_user: User, service_stub) -> TestClient:
    app.dependency_overrides[get_db] = _db_override
    app.dependency_overrides[get_current_active_user] = lambda: current_user
    app.dependency_overrides[get_visit_service] = lambda: service_stub
    return TestClient(app, raise_server_exceptions=False)


def teardown_function() -> None:
    app.dependency_overrides.clear()


CREATE_PAYLOAD = {
    "chief_complaint": "progressive tremor",
    "history": "six months",
    "vitals": {"heart_rate": 72},
    "symptoms": [{"symptom_name": "tremor", "severity": 4, "onset": "gradual"}],
}


# --------------------------------------------------------------------------
# Create and read
# --------------------------------------------------------------------------


def test_create_visit_returns_201_with_symptoms_and_draft_status() -> None:
    clinician = _user()
    patient_id = uuid4()
    created = _visit(patient_id)

    class ServiceStub:
        def create_visit(self, db, pid, visit_data, current_user):
            assert pid == patient_id
            assert current_user is clinician
            assert visit_data.symptoms[0].symptom_name == "tremor"
            return created

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/patients/{patient_id}/visits", json=CREATE_PAYLOAD
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == str(created.id)
    assert body["patient_id"] == str(patient_id)
    assert body["status"] == "draft"
    assert [s["symptom_name"] for s in body["symptoms"]] == ["tremor"]
    assert body["vitals"]["heart_rate"] == 72


def test_create_visit_for_another_doctors_patient_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def create_visit(self, db, pid, visit_data, current_user):
            raise EntityNotFoundError("Patient", pid)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/patients/{uuid4()}/visits", json=CREATE_PAYLOAD
    )

    assert response.status_code == 404
    assert response.json()["error_code"] == "not_found"


def test_get_own_visit_succeeds() -> None:
    clinician = _user()
    visit = _visit()

    class ServiceStub:
        def get_visit(self, db, visit_id, current_user):
            assert current_user is clinician
            return visit

    response = _client(clinician, ServiceStub()).get(f"/api/v1/visits/{visit.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(visit.id)


def test_visit_response_does_not_embed_the_patient_object() -> None:
    """Only patient_id is exposed, so no endpoint can lazy-load per row."""
    clinician = _user()
    visit = _visit()

    class ServiceStub:
        def get_visit(self, db, visit_id, current_user):
            return visit

    body = _client(clinician, ServiceStub()).get(f"/api/v1/visits/{visit.id}").json()

    assert "patient_id" in body
    assert "patient" not in body
    assert "doctor" not in body


# --------------------------------------------------------------------------
# ADR-001 / ADR-002 parity
# --------------------------------------------------------------------------


def test_unauthorized_visit_and_missing_visit_return_identical_404() -> None:
    clinician = _user()
    other_doctors_visit_id = uuid4()
    nonexistent_id = uuid4()

    class NotFoundServiceStub:
        def get_visit(self, db, visit_id, current_user):
            raise EntityNotFoundError("Visit", visit_id)

    client = _client(clinician, NotFoundServiceStub())
    owned_by_other = client.get(f"/api/v1/visits/{other_doctors_visit_id}")
    truly_missing = client.get(f"/api/v1/visits/{nonexistent_id}")

    assert owned_by_other.status_code == truly_missing.status_code == 404
    assert owned_by_other.json()["error_code"] == truly_missing.json()["error_code"]
    assert set(owned_by_other.json().keys()) == set(truly_missing.json().keys())
    # The masked 404 must not name the parent resource at all.
    assert "Patient" not in owned_by_other.text
    assert "Patient" not in truly_missing.text


def test_update_on_another_doctors_visit_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def update_visit(self, db, visit_id, visit_data, current_user):
            raise EntityNotFoundError("Visit", visit_id)

    response = _client(clinician, ServiceStub()).patch(
        f"/api/v1/visits/{uuid4()}", json={"chief_complaint": "edited"}
    )

    assert response.status_code == 404
    assert "Patient" not in response.text


def test_delete_on_another_doctors_visit_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def delete_visit(self, db, visit_id, current_user):
            raise EntityNotFoundError("Visit", visit_id)

    response = _client(clinician, ServiceStub()).delete(f"/api/v1/visits/{uuid4()}")

    assert response.status_code == 404
    assert "Patient" not in response.text


def test_delete_own_visit_returns_204() -> None:
    clinician = _user()
    deleted = []

    class ServiceStub:
        def delete_visit(self, db, visit_id, current_user):
            deleted.append(visit_id)

    visit_id = uuid4()
    response = _client(clinician, ServiceStub()).delete(f"/api/v1/visits/{visit_id}")

    assert response.status_code == 204
    assert response.content == b""
    assert deleted == [visit_id]


# --------------------------------------------------------------------------
# Collections
# --------------------------------------------------------------------------


def test_list_visits_returns_page_based_pagination_shape() -> None:
    clinician = _user()
    patient_id = uuid4()

    class ServiceStub:
        def list_patient_visits(
            self, db, pid, current_user, skip, limit, status=None
        ):
            assert skip == 20
            assert limit == 20
            return [_visit(pid)], 41

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/patients/{patient_id}/visits", params={"page": 2, "page_size": 20}
    )

    assert response.status_code == 200
    assert response.json()["pagination"] == {
        "page": 2,
        "page_size": 20,
        "total_records": 41,
        "total_pages": 3,
    }


def test_list_visits_passes_the_status_filter_through() -> None:
    clinician = _user()
    seen = []

    class ServiceStub:
        def list_patient_visits(
            self, db, pid, current_user, skip, limit, status=None
        ):
            seen.append(status)
            return [], 0

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/patients/{uuid4()}/visits", params={"status": "closed"}
    )

    assert response.status_code == 200
    assert seen == [VisitStatus.CLOSED]


def test_list_visits_for_another_doctors_patient_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def list_patient_visits(
            self, db, pid, current_user, skip, limit, status=None
        ):
            raise EntityNotFoundError("Patient", pid)

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/patients/{uuid4()}/visits"
    )

    assert response.status_code == 404


# --------------------------------------------------------------------------
# History
# --------------------------------------------------------------------------


def test_history_route_is_not_shadowed_and_returns_newest_first() -> None:
    clinician = _user()
    patient_id = uuid4()

    class ServiceStub:
        def get_patient_history(
            self, db, pid, current_user, *, limit, newest_first, exclude_visit_id
        ):
            assert pid == patient_id
            assert limit == 10
            assert newest_first is True
            assert exclude_visit_id is None
            return [
                _visit(pid, days_offset=60),
                _visit(pid, days_offset=30),
                _visit(pid, days_offset=0),
            ], 3

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/patients/{patient_id}/visits/history"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["patient_id"] == str(patient_id)
    assert body["order"] == "desc"
    assert body["total_visits"] == 3
    assert body["returned"] == 3
    dates = [visit["visit_date"] for visit in body["visits"]]
    assert dates == sorted(dates, reverse=True)
    # Symptoms travel with each visit -- this is the AI-01 input payload.
    assert body["visits"][0]["symptoms"]


def test_history_accepts_an_ascending_window_excluding_the_current_visit() -> None:
    clinician = _user()
    current_visit_id = uuid4()

    class ServiceStub:
        def get_patient_history(
            self, db, pid, current_user, *, limit, newest_first, exclude_visit_id
        ):
            assert limit == 3
            assert newest_first is False
            assert exclude_visit_id == current_visit_id
            return [_visit(pid)], 9

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/patients/{uuid4()}/visits/history",
        params={
            "limit": 3,
            "order": "asc",
            "exclude_visit_id": str(current_visit_id),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["order"] == "asc"
    assert body["total_visits"] == 9
    assert body["returned"] == 1


def test_history_rejects_an_out_of_range_window() -> None:
    clinician = _user()

    class ServiceStub:
        def get_patient_history(self, db, pid, current_user, **kwargs):
            raise AssertionError("service must not be reached")

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/patients/{uuid4()}/visits/history", params={"limit": 500}
    )

    assert response.status_code == 422


def test_history_for_another_doctors_patient_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def get_patient_history(self, db, pid, current_user, **kwargs):
            raise EntityNotFoundError("Patient", pid)

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/patients/{uuid4()}/visits/history"
    )

    assert response.status_code == 404


# --------------------------------------------------------------------------
# Symptoms
# --------------------------------------------------------------------------


def test_add_symptom_returns_201() -> None:
    clinician = _user()
    visit_id = uuid4()

    class ServiceStub:
        def add_symptom(self, db, vid, symptom_data, current_user):
            assert vid == visit_id
            return _symptom(vid, name=symptom_data.symptom_name)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{visit_id}/symptoms",
        json={"symptom_name": "ataxia", "severity": 7},
    )

    assert response.status_code == 201
    assert response.json()["symptom_name"] == "ataxia"
    assert response.json()["visit_id"] == str(visit_id)


def test_list_symptoms_returns_pagination_shape() -> None:
    clinician = _user()
    visit_id = uuid4()

    class ServiceStub:
        def list_symptoms(self, db, vid, current_user, skip, limit):
            return [_symptom(vid)], 1

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/visits/{visit_id}/symptoms"
    )

    assert response.status_code == 200
    assert response.json()["pagination"] == {
        "page": 1,
        "page_size": 20,
        "total_records": 1,
        "total_pages": 1,
    }


def test_symptom_from_a_mismatched_visit_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def update_symptom(self, db, vid, sid, symptom_data, current_user):
            raise EntityNotFoundError("Symptom", sid)

    response = _client(clinician, ServiceStub()).patch(
        f"/api/v1/visits/{uuid4()}/symptoms/{uuid4()}", json={"severity": 9}
    )

    assert response.status_code == 404


def test_symptom_on_another_doctors_visit_is_a_visit_shaped_404() -> None:
    clinician = _user()

    class ServiceStub:
        def delete_symptom(self, db, vid, sid, current_user):
            raise EntityNotFoundError("Visit", vid)

    response = _client(clinician, ServiceStub()).delete(
        f"/api/v1/visits/{uuid4()}/symptoms/{uuid4()}"
    )

    assert response.status_code == 404
    assert "Patient" not in response.text


def test_delete_symptom_returns_204() -> None:
    clinician = _user()

    class ServiceStub:
        def delete_symptom(self, db, vid, sid, current_user):
            return None

    response = _client(clinician, ServiceStub()).delete(
        f"/api/v1/visits/{uuid4()}/symptoms/{uuid4()}"
    )

    assert response.status_code == 204


# --------------------------------------------------------------------------
# Validation contract
# --------------------------------------------------------------------------


def test_severity_outside_the_clinical_scale_is_rejected() -> None:
    clinician = _user()

    class ServiceStub:
        def add_symptom(self, db, vid, symptom_data, current_user):
            raise AssertionError("service must not be reached")

    client = _client(clinician, ServiceStub())
    visit_id = uuid4()

    for severity in (0, 11):
        response = client.post(
            f"/api/v1/visits/{visit_id}/symptoms",
            json={"symptom_name": "tremor", "severity": severity},
        )
        assert response.status_code == 422, severity


def test_unknown_onset_value_is_rejected() -> None:
    clinician = _user()

    class ServiceStub:
        def add_symptom(self, db, vid, symptom_data, current_user):
            raise AssertionError("service must not be reached")

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/symptoms",
        json={"symptom_name": "tremor", "severity": 5, "onset": "sideways"},
    )

    assert response.status_code == 422


def test_a_whitespace_only_observation_is_rejected() -> None:
    clinician = _user()

    class ServiceStub:
        def add_symptom(self, db, vid, symptom_data, current_user):
            raise AssertionError("service must not be reached")

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/symptoms",
        json={"symptom_name": "tremor", "severity": 5, "observation": "   "},
    )

    assert response.status_code == 422


def test_an_oversized_observation_is_rejected() -> None:
    clinician = _user()

    class ServiceStub:
        def add_symptom(self, db, vid, symptom_data, current_user):
            raise AssertionError("service must not be reached")

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/symptoms",
        json={"symptom_name": "tremor", "severity": 5, "observation": "x" * 2001},
    )

    assert response.status_code == 422


def test_unknown_vitals_field_is_rejected() -> None:
    clinician = _user()

    class ServiceStub:
        def create_visit(self, db, pid, visit_data, current_user):
            raise AssertionError("service must not be reached")

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/patients/{uuid4()}/visits",
        json={"chief_complaint": "tremor", "vitals": {"mmse_score": 24}},
    )

    assert response.status_code == 422


def test_setting_the_ai_owned_status_is_rejected() -> None:
    clinician = _user()

    class ServiceStub:
        def create_visit(self, db, pid, visit_data, current_user):
            raise ValidationApplicationError(
                "Status 'analyzed' is set by the analysis pipeline "
                "and cannot be assigned through the visits API."
            )

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/patients/{uuid4()}/visits",
        json={"chief_complaint": "tremor", "status": "analyzed"},
    )

    assert response.status_code == 422
    assert response.json()["error_code"] == "validation_error"

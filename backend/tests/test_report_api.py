"""Contract tests for the report endpoints.

Beyond the usual status/shape assertions: a cross-clinician report 404s
without naming its analysis, a rendering failure is a controlled 500, and
the PDF download carries the headers ADR-004 requires.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies import (
    get_current_active_user,
    get_db,
    get_report_service,
)
from app.models.report import Report
from app.models.user import User, UserRole
from app.schemas.analysis import DISCLAIMER
from app.utils.exceptions import EntityNotFoundError, InternalServerError
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


def _snapshot() -> dict:
    return {
        "analysis_id": str(uuid4()),
        "visit_id": str(uuid4()),
        "patient": {"full_name": "Ada Lovelace", "age_years": 62, "gender": "F"},
        "visit": {
            "visit_date": NOW.isoformat(),
            "chief_complaint": "intermittent hand tremor",
            "symptoms": [],
        },
        "model_name": "neuroone-mock-reasoner-v1",
        "provider_mode": "simulated",
        "pipeline_note": "pipeline complete, evidence retrieval simulated",
        "disclaimer": DISCLAIMER,
        "generated_at": NOW.isoformat(),
        "findings": [
            {
                "rank": 0,
                "condition_name": "Parkinsonian syndrome",
                "category": "differential_diagnosis",
                "likelihood_band": "moderate",
                "supporting_findings": ["resting tremor severity 8"],
                "contradicting_findings": [],
                "explanation": "Motor findings are consistent with...",
                "trend_basis": [],
                "evidence": [
                    {
                        "source": "Journal of Neurology",
                        "citation": "Doe J et al., 2024.",
                        "relevant_passage": "Progressive resting tremor.",
                    }
                ],
            }
        ],
    }


def _report(analysis_id=None, **overrides) -> Report:
    now = datetime.now(timezone.utc)
    payload = {
        "id": uuid4(),
        "analysis_id": analysis_id or uuid4(),
        "generated_by_id": uuid4(),
        "generated_at": NOW,
        "filename": "neuroone-report-placeholder.pdf",
        "snapshot": _snapshot(),
        "created_at": now,
        "updated_at": now,
    }
    payload.update(overrides)
    return Report(**payload)


def _db_override():
    yield object()


def _client(current_user: User, service_stub) -> TestClient:
    app.dependency_overrides[get_db] = _db_override
    app.dependency_overrides[get_current_active_user] = lambda: current_user
    app.dependency_overrides[get_report_service] = lambda: service_stub
    return TestClient(app, raise_server_exceptions=False)


def teardown_function() -> None:
    app.dependency_overrides.clear()


# --------------------------------------------------------------------------
# Generation
# --------------------------------------------------------------------------


def test_generating_a_report_returns_201_with_metadata() -> None:
    clinician = _user()
    analysis_id = uuid4()
    created = _report(analysis_id)

    class ServiceStub:
        def generate_report(self, db, aid, current_user):
            assert aid == analysis_id
            assert current_user is clinician
            return created

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/analyses/{analysis_id}/reports"
    )

    assert response.status_code == 201
    body = response.json()
    assert body["analysis_id"] == str(analysis_id)
    assert body["filename"] == "neuroone-report-placeholder.pdf"
    assert "snapshot" not in body


def test_generating_on_another_clinicians_analysis_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def generate_report(self, db, aid, current_user):
            raise EntityNotFoundError("Analysis", aid)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/analyses/{uuid4()}/reports"
    )

    assert response.status_code == 404


def test_a_rendering_failure_is_a_controlled_500() -> None:
    clinician = _user()

    class ServiceStub:
        def generate_report(self, db, aid, current_user):
            raise InternalServerError(
                "Report rendering failed.", error_code="report_render_error"
            )

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/analyses/{uuid4()}/reports"
    )

    assert response.status_code == 500
    assert response.json()["error_code"] == "report_render_error"


# --------------------------------------------------------------------------
# Listing
# --------------------------------------------------------------------------


def test_listing_reports_returns_the_pagination_envelope() -> None:
    clinician = _user()
    analysis_id = uuid4()

    class ServiceStub:
        def list_analysis_reports(self, db, aid, current_user, skip, limit):
            assert skip == 20
            assert limit == 20
            return [_report(aid)], 41

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/analyses/{analysis_id}/reports",
        params={"page": 2, "page_size": 20},
    )

    assert response.status_code == 200
    assert response.json()["pagination"] == {
        "page": 2,
        "page_size": 20,
        "total_records": 41,
        "total_pages": 3,
    }


def test_listing_a_foreign_analysiss_reports_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def list_analysis_reports(self, db, aid, current_user, skip, limit):
            raise EntityNotFoundError("Analysis", aid)

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/analyses/{uuid4()}/reports"
    )

    assert response.status_code == 404


# --------------------------------------------------------------------------
# Reads
# --------------------------------------------------------------------------


def test_get_report_by_id_succeeds() -> None:
    clinician = _user()
    report = _report()

    class ServiceStub:
        def get_report(self, db, report_id, current_user):
            return report

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/reports/{report.id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(report.id)


def test_a_foreign_report_404s_without_naming_its_analysis() -> None:
    clinician = _user()

    class ServiceStub:
        def get_report(self, db, report_id, current_user):
            raise EntityNotFoundError("Report", report_id)

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/reports/{uuid4()}"
    )

    assert response.status_code == 404
    assert "Analysis" not in response.text
    assert "Visit" not in response.text


# --------------------------------------------------------------------------
# PDF download
# --------------------------------------------------------------------------


def test_downloading_the_pdf_returns_protected_headers() -> None:
    clinician = _user()

    class ServiceStub:
        def get_pdf(self, db, report_id, current_user):
            return b"%PDF-1.4 minimal", "neuroone-report-x.pdf"

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/reports/{uuid4()}/pdf"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert (
        response.headers["content-disposition"]
        == 'attachment; filename="neuroone-report-x.pdf"'
    )
    assert response.headers["cache-control"] == "private, no-store"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.content == b"%PDF-1.4 minimal"


def test_downloading_a_foreign_reports_pdf_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def get_pdf(self, db, report_id, current_user):
            raise EntityNotFoundError("Report", report_id)

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/reports/{uuid4()}/pdf"
    )

    assert response.status_code == 404


def test_downloading_a_report_that_fails_to_render_is_a_controlled_500() -> None:
    clinician = _user()

    class ServiceStub:
        def get_pdf(self, db, report_id, current_user):
            raise InternalServerError(
                "Report rendering failed.", error_code="report_render_error"
            )

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/reports/{uuid4()}/pdf"
    )

    assert response.status_code == 500
    assert response.json()["error_code"] == "report_render_error"


# --------------------------------------------------------------------------
# Route surface
# --------------------------------------------------------------------------


def test_reports_are_not_exposed_as_a_diagnosis_endpoint() -> None:
    """AGENTS.md 8.2: not in the schema, not in API field naming."""
    paths = app.openapi()["paths"]

    assert not [p for p in paths if "/diagnosis" in p]

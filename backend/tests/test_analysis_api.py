"""Contract tests for the analysis endpoints.

Beyond the usual status/shape assertions, two checks are deliberate: that an
AIError reaches the client as a 502 through the centralized error path, and
that no serialized response ever contains a definitive-diagnosis field name.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies import (
    get_analysis_service,
    get_current_active_user,
    get_db,
)
from app.models.analysis import (
    Analysis,
    AnalysisEvidence,
    AnalysisFinding,
    FindingCategory,
)
from app.models.user import User, UserRole
from app.schemas.analysis import DISCLAIMER, SIMULATED_PIPELINE_NOTE
from app.utils.exceptions import AIError, EntityNotFoundError
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


def _evidence(rank=0) -> AnalysisEvidence:
    now = datetime.now(timezone.utc)
    return AnalysisEvidence(
        id=uuid4(),
        finding_id=uuid4(),
        rank=rank,
        source="Simulated Source",
        citation="Illustrative reference (simulated corpus), 2024.",
        relevant_passage="A passage.",
        document_id="doc-1",
        chunk_id="doc-1#c1",
        source_tier="guideline",
        published_year=2024,
        relevance_score=1.0,
        created_at=now,
        updated_at=now,
    )


def _finding(rank=0, *, name="Parkinsonian syndrome", category=None, trend=()):
    now = datetime.now(timezone.utc)
    finding = AnalysisFinding(
        id=uuid4(),
        analysis_id=uuid4(),
        rank=rank,
        condition_name=name,
        category=category or FindingCategory.DIFFERENTIAL_DIAGNOSIS,
        confidence=0.55,
        supporting_findings=["tremor recorded at severity 8"],
        contradicting_findings=[],
        explanation="an explanation",
        trend_basis=list(trend),
        created_at=now,
        updated_at=now,
    )
    finding.evidence = [_evidence()]
    return finding


def _analysis(visit_id=None, *, findings=None) -> Analysis:
    now = datetime.now(timezone.utc)
    analysis = Analysis(
        id=uuid4(),
        visit_id=visit_id or uuid4(),
        requested_by_id=uuid4(),
        model_name="neuroone-mock-reasoner-v1",
        provider_mode="simulated",
        pipeline_note=SIMULATED_PIPELINE_NOTE,
        disclaimer=DISCLAIMER,
        generated_at=NOW,
        context_snapshot={"patient_age_years": 62},
        created_at=now,
        updated_at=now,
    )
    analysis.findings = list(findings) if findings is not None else [_finding()]
    return analysis


def _db_override():
    yield object()


def _client(current_user: User, service_stub) -> TestClient:
    app.dependency_overrides[get_db] = _db_override
    app.dependency_overrides[get_current_active_user] = lambda: current_user
    app.dependency_overrides[get_analysis_service] = lambda: service_stub
    return TestClient(app, raise_server_exceptions=False)


def teardown_function() -> None:
    app.dependency_overrides.clear()


# --------------------------------------------------------------------------
# Trigger
# --------------------------------------------------------------------------


def test_triggering_analysis_returns_201_with_findings_and_citations() -> None:
    clinician = _user()
    visit_id = uuid4()
    created = _analysis(visit_id)

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            assert vid == visit_id
            assert current_user is clinician
            assert history_limit == 10
            return created

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{visit_id}/analyses", json={}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["visit_id"] == str(visit_id)
    assert body["findings"][0]["name"] == "Parkinsonian syndrome"
    assert body["findings"][0]["evidence"][0]["citation"]
    assert body["findings"][0]["evidence"][0]["document_id"] == "doc-1"
    assert body["findings"][0]["evidence"][0]["chunk_id"] == "doc-1#c1"
    assert body["findings"][0]["likelihood_band"] == "moderate"


def test_an_empty_body_is_valid_so_the_demo_can_just_post() -> None:
    clinician = _user()
    seen = []

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            seen.append(history_limit)
            return _analysis(vid)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/analyses", json={}
    )

    assert response.status_code == 201
    assert seen == [10]


def test_history_limit_is_passed_through() -> None:
    clinician = _user()
    seen = []

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            seen.append(history_limit)
            return _analysis(vid)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/analyses", json={"history_limit": 3}
    )

    assert response.status_code == 201
    assert seen == [3]


def test_an_out_of_range_history_limit_is_rejected() -> None:
    clinician = _user()

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            raise AssertionError("service must not be reached")

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/analyses", json={"history_limit": 500}
    )

    assert response.status_code == 422


def test_provenance_is_visible_on_the_wire() -> None:
    """A consumer must be able to tell simulated evidence from live evidence."""
    clinician = _user()

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            return _analysis(vid)

    body = (
        _client(clinician, ServiceStub())
        .post(f"/api/v1/visits/{uuid4()}/analyses", json={})
        .json()
    )

    assert body["provider_mode"] == "simulated"
    assert "simulated" in body["pipeline_note"]
    assert "not a diagnosis" in body["disclaimer"].lower()


def test_the_context_snapshot_is_not_exposed() -> None:
    clinician = _user()

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            return _analysis(vid)

    body = (
        _client(clinician, ServiceStub())
        .post(f"/api/v1/visits/{uuid4()}/analyses", json={})
        .json()
    )

    assert "context_snapshot" not in body


# --------------------------------------------------------------------------
# Safety-boundary naming
# --------------------------------------------------------------------------


def test_no_response_field_frames_output_as_a_definitive_diagnosis() -> None:
    """AGENTS.md 8.2: not in the schema, not in API field naming."""
    clinician = _user()

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            return _analysis(vid)

    text = (
        _client(clinician, ServiceStub())
        .post(f"/api/v1/visits/{uuid4()}/analyses", json={})
        .text
    )

    for forbidden in (
        "final_diagnosis",
        "doctor_verified",
        "certainty",
        "probability",
    ):
        assert forbidden not in text, forbidden


def test_an_early_watch_finding_serializes_its_trend_basis() -> None:
    clinician = _user()
    trend = [
        {
            "visit_id": str(uuid4()),
            "symptom_id": str(uuid4()),
            "symptom_name": "memory loss",
            "severity": 4,
            "observation": "memory loss severity 2 -> 4 across 3 visits",
        }
    ]

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            return _analysis(
                vid,
                findings=[
                    _finding(
                        0,
                        name="Progressive amnestic cognitive impairment",
                        category=FindingCategory.EARLY_WATCH,
                        trend=trend,
                    )
                ],
            )

    body = (
        _client(clinician, ServiceStub())
        .post(f"/api/v1/visits/{uuid4()}/analyses", json={})
        .json()
    )

    finding = body["findings"][0]
    assert finding["category"] == "early_watch"
    assert finding["trend_basis"][0]["symptom_name"] == "memory loss"


# --------------------------------------------------------------------------
# Failure handling through the centralized error path
# --------------------------------------------------------------------------


def test_an_ai_failure_is_a_502_carrying_its_error_code() -> None:
    clinician = _user()

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            raise AIError(
                "The analysis model is unavailable.", error_code="ai_error"
            )

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/analyses", json={}
    )

    assert response.status_code == 502
    assert response.json()["error_code"] == "ai_error"


def test_a_retrieval_failure_is_distinguishable_from_a_model_failure() -> None:
    clinician = _user()

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            raise AIError("Retrieval down.", error_code="rag_error")

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/analyses", json={}
    )

    assert response.status_code == 502
    assert response.json()["error_code"] == "rag_error"


def test_triggering_analysis_on_another_clinicians_visit_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def analyze_visit(self, db, vid, current_user, *, history_limit):
            raise EntityNotFoundError("Visit", vid)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/visits/{uuid4()}/analyses", json={}
    )

    assert response.status_code == 404
    assert "Patient" not in response.text


# --------------------------------------------------------------------------
# Sign-off (ADR-006 decision 6)
# --------------------------------------------------------------------------


def test_signing_off_an_analysis_returns_the_reviewed_analysis() -> None:
    clinician = _user()
    analysis = _analysis()
    analysis.reviewed_by_id = clinician.id
    analysis.reviewed_at = NOW

    class ServiceStub:
        def sign_off_analysis(self, db, analysis_id, current_user):
            assert analysis_id == analysis.id
            assert current_user is clinician
            return analysis

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/analyses/{analysis.id}/review"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["reviewed_by_id"] == str(clinician.id)
    assert body["reviewed_at"] is not None


def test_signing_off_a_foreign_analysis_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def sign_off_analysis(self, db, analysis_id, current_user):
            raise EntityNotFoundError("Analysis", analysis_id)

    response = _client(clinician, ServiceStub()).post(
        f"/api/v1/analyses/{uuid4()}/review"
    )

    assert response.status_code == 404


# --------------------------------------------------------------------------
# Reads
# --------------------------------------------------------------------------


def test_get_analysis_by_id_succeeds() -> None:
    clinician = _user()
    analysis = _analysis()

    class ServiceStub:
        def get_analysis(self, db, analysis_id, current_user):
            return analysis

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/analyses/{analysis.id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(analysis.id)


def test_a_foreign_analysis_404s_without_naming_its_visit() -> None:
    clinician = _user()

    class ServiceStub:
        def get_analysis(self, db, analysis_id, current_user):
            raise EntityNotFoundError("Analysis", analysis_id)

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/analyses/{uuid4()}"
    )

    assert response.status_code == 404
    assert "Visit" not in response.text
    assert "Patient" not in response.text


def test_listing_analyses_returns_the_pagination_envelope() -> None:
    clinician = _user()
    visit_id = uuid4()

    class ServiceStub:
        def list_visit_analyses(self, db, vid, current_user, skip, limit):
            assert skip == 20
            assert limit == 20
            return [_analysis(vid)], 41

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/visits/{visit_id}/analyses",
        params={"page": 2, "page_size": 20},
    )

    assert response.status_code == 200
    assert response.json()["pagination"] == {
        "page": 2,
        "page_size": 20,
        "total_records": 41,
        "total_pages": 3,
    }


def test_latest_route_is_not_shadowed_by_the_item_route() -> None:
    clinician = _user()
    visit_id = uuid4()
    latest = _analysis(visit_id)

    class ServiceStub:
        def get_latest_for_visit(self, db, vid, current_user):
            assert vid == visit_id
            return latest

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/visits/{visit_id}/analyses/latest"
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(latest.id)


def test_latest_is_404_before_a_case_has_been_analyzed() -> None:
    clinician = _user()

    class ServiceStub:
        def get_latest_for_visit(self, db, vid, current_user):
            raise EntityNotFoundError("Analysis")

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/visits/{uuid4()}/analyses/latest"
    )

    assert response.status_code == 404


def test_listing_a_foreign_visits_analyses_is_404() -> None:
    clinician = _user()

    class ServiceStub:
        def list_visit_analyses(self, db, vid, current_user, skip, limit):
            raise EntityNotFoundError("Visit", vid)

    response = _client(clinician, ServiceStub()).get(
        f"/api/v1/visits/{uuid4()}/analyses"
    )

    assert response.status_code == 404


# --------------------------------------------------------------------------
# Route surface
# --------------------------------------------------------------------------


def test_no_diagnosis_or_rag_prefix_is_advertised() -> None:
    """An OpenAPI tag named "diagnosis" is the framing 8.2 forbids."""
    paths = app.openapi()["paths"]

    assert not [p for p in paths if "/diagnosis" in p or "/rag" in p]

    tags = {
        tag
        for path in paths.values()
        for operation in path.values()
        for tag in operation.get("tags", [])
    }
    assert "diagnosis" not in tags
    assert "rag" not in tags

"""Health endpoint failure-safety tests."""

from fastapi.testclient import TestClient

from main import app


def test_health_failure_is_non_200_and_does_not_leak_exception(monkeypatch) -> None:
    secret = "private connection string and database failure"

    def fail_connect():
        raise RuntimeError(secret)

    monkeypatch.setattr("app.main.engine.connect", fail_connect)
    response = TestClient(app, raise_server_exceptions=False).get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "unhealthy"}
    assert secret not in response.text

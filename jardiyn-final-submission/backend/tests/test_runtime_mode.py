from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_reports_mock_mode_by_default(monkeypatch):
    monkeypatch.delenv("LLM_MODE", raising=False)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["llm_mode"] == "mock"


def test_health_reports_live_mode_when_enabled(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "live")

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["llm_mode"] == "live"


def test_backend_allows_github_pages_origin_for_chat_preflight():
    response = client.options(
        "/api/agent/chat",
        headers={
            "Origin": "https://endersra.github.io",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code in (200, 204)
    assert response.headers.get("access-control-allow-origin") == "https://endersra.github.io"

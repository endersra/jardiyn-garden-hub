from pathlib import Path
import importlib.util

from fastapi.testclient import TestClient


MAIN_PATH = Path(__file__).resolve().parents[1] / "main.py"
spec = importlib.util.spec_from_file_location("jardiyn_backend_main", MAIN_PATH)
main = importlib.util.module_from_spec(spec)

assert spec is not None
assert spec.loader is not None

spec.loader.exec_module(main)

client = TestClient(main.app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "jardiyn-agent-backend"
    assert data["phase"] == "phase-3-live-agent-runtime"
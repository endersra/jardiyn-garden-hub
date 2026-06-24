from pathlib import Path
import importlib.util

from fastapi.testclient import TestClient


MAIN_PATH = Path(__file__).resolve().parents[1] / "main.py"
spec = importlib.util.spec_from_file_location("jardiyn_backend_main_chat", MAIN_PATH)
main = importlib.util.module_from_spec(spec)

assert spec is not None
assert spec.loader is not None

spec.loader.exec_module(main)

client = TestClient(main.app)


def test_agent_chat_route_returns_trace():
    response = client.post(
        "/api/agent/chat",
        json={
            "message": "My basil leaves are yellow and the soil is soggy.",
            "user_id": "demo-user",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "tasks" in data
    assert "review" in data
    assert "trace" in data

    agents = [step["agent"] for step in data["trace"]]

    assert "orchestrator" in agents
    assert "garden_memory_tool" in agents
    assert "seasonal_context_tool" in agents
    assert "garden_reasoner" in agents
    assert "reviewer" in agents

    assert data["trace"][3]["source"] == "mock_llm_client"
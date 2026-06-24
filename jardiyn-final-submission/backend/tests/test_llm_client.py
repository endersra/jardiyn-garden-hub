import os

from agents.llm_client import generate_response


def test_llm_client_mock_mode_returns_traceable_response(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "mock")

    result = generate_response(
        prompt="My basil leaves are yellow and the soil is soggy.",
        model_role="garden_reasoner",
    )

    assert result["source"] == "mock_llm_client"
    assert result["model"] == "mock-claude-garden-reasoner"
    assert "basil" in result["text"].lower()
    assert result["model_role"] == "garden_reasoner"


def test_llm_client_live_mode_requires_api_key(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "live")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    try:
        generate_response(
            prompt="Test prompt",
            model_role="garden_reasoner",
        )
    except RuntimeError as error:
        assert "ANTHROPIC_API_KEY is required" in str(error)
    else:
        raise AssertionError("Expected RuntimeError when API key is missing")
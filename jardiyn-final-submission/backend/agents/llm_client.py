import os
from typing import Any


def generate_response(prompt: str, model_role: str = "garden_reasoner") -> dict[str, Any]:
    """
    Mock-mode LLM client for Phase 3 agent runtime.
    Live Claude wiring will be added after the agent route is proven.
    """
    llm_mode = os.getenv("LLM_MODE", "mock")

    if llm_mode != "mock":
        raise RuntimeError(
            "Live Claude mode is not wired yet. Set LLM_MODE=mock for this milestone."
        )

    return {
        "text": (
            "Your basil is likely stressed from overwatering. "
            "Because the soil is soggy and the leaves are yellow, pause watering, "
            "check drainage, and let the top inch of soil dry before watering again."
        ),
        "model": "mock-claude-garden-reasoner",
        "source": "mock_llm_client",
        "model_role": model_role,
    }
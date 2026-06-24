import os
from typing import Any

from anthropic import Anthropic


def _mock_response(model_role: str) -> dict[str, Any]:
    return {
        "text": (
            "Your basil is likely stressed from overwatering. "
            "Because the soil is soggy and the leaves are yellow, pause watering, "
            "check drainage, and let the top inch of soil dry before watering again."
        ),
        "model": "mock-claude-garden-reasoner",
        "source": "mock_llm_client",
        "model_role": model_role,
        "usage": None,
    }


def generate_response(prompt: str, model_role: str = "garden_reasoner") -> dict[str, Any]:
    """
    LLM client for JarDIYn Phase 3.

    LLM_MODE=mock:
        Returns a deterministic mock response for tests and offline demos.

    LLM_MODE=live:
        Calls Claude through the Anthropic Python SDK.
    """
    llm_mode = os.getenv("LLM_MODE", "mock").lower()

    if llm_mode == "mock":
        return _mock_response(model_role)

    if llm_mode != "live":
        raise RuntimeError(f"Unsupported LLM_MODE: {llm_mode}")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is required when LLM_MODE=live. "
            "Set it as an environment variable; never commit it to GitHub."
        )

    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

    client = Anthropic(api_key=api_key)

    message = client.messages.create(
        model=model,
        max_tokens=700,
        temperature=0.2,
        system=(
            "You are the JarDIYn garden reasoning agent. "
            "Give beginner-friendly, safe, practical gardening guidance. "
            "Use the provided garden profile and seasonal context. "
            "Avoid unsafe chemical advice. Explain uncertainty."
        ),
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    text_parts: list[str] = []
    for block in message.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)

    return {
        "text": "\n".join(text_parts).strip(),
        "model": model,
        "source": "anthropic_api",
        "model_role": model_role,
        "usage": {
            "input_tokens": getattr(message.usage, "input_tokens", None),
            "output_tokens": getattr(message.usage, "output_tokens", None),
        },
    }
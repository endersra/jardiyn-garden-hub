from typing import Any

from agents.llm_client import generate_response


def run_garden_reasoner(
    user_message: str,
    garden_profile: dict[str, Any],
    seasonal_context: dict[str, Any],
) -> dict[str, Any]:
    prompt = f"""
User message:
{user_message}

Garden profile:
{garden_profile}

Seasonal context:
{seasonal_context}

Return beginner-friendly gardening guidance with likely issue, reasoning, confidence, and tasks.
"""

    llm_result = generate_response(prompt, model_role="garden_reasoner")

    return {
        "answer": llm_result["text"],
        "confidence": "medium",
        "tasks": [
            "Pause watering for 2 days.",
            "Check that the pot has drainage holes.",
            "Let the top inch of soil dry before watering again.",
        ],
        "model": llm_result["model"],
        "source": llm_result["source"],
    }
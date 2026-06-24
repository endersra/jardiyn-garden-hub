from typing import Any

from agents.garden_reasoner import run_garden_reasoner
from agents.reviewer import review_response
from tools.garden_memory import get_garden_profile
from tools.seasonal_context import get_seasonal_context


def run_chat_workflow(user_message: str, user_id: str = "demo-user") -> dict[str, Any]:
    trace: list[dict[str, Any]] = []

    trace.append({
        "step": 1,
        "agent": "orchestrator",
        "action": "classified request as plant-care-chat",
        "source": "backend",
    })

    garden_profile = get_garden_profile(user_id)
    trace.append({
        "step": 2,
        "agent": "garden_memory_tool",
        "action": "retrieved user garden profile and plant history",
        "source": "backend_memory",
    })

    plant = "basil" if "basil" in user_message.lower() else None
    seasonal_context = get_seasonal_context(garden_profile["location"], plant)
    trace.append({
        "step": 3,
        "agent": "seasonal_context_tool",
        "action": "added regional and seasonal context",
        "source": "local_reference_data",
    })

    reasoner_output = run_garden_reasoner(user_message, garden_profile, seasonal_context)
    trace.append({
        "step": 4,
        "agent": "garden_reasoner",
        "action": "generated recommendation",
        "model": reasoner_output["model"],
        "source": reasoner_output["source"],
    })

    review = review_response(reasoner_output)
    trace.append({
        "step": 5,
        "agent": "reviewer",
        "action": "checked safety, clarity, and usefulness",
        "source": "backend_reviewer",
    })

    return {
        "answer": review["final_answer"],
        "confidence": reasoner_output["confidence"],
        "tasks": reasoner_output["tasks"],
        "review": {
            "approved": review["approved"],
            "notes": review["notes"],
        },
        "trace": trace,
    }
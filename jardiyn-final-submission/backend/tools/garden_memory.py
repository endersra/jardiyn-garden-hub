from typing import Any


def get_garden_profile(user_id: str = "demo-user") -> dict[str, Any]:
    return {
        "user_id": user_id,
        "location": "Michigan",
        "zone": "6a",
        "skill_level": "beginner",
        "plants": ["basil", "tomato", "pothos"],
        "watering_history": {
            "basil": "watered frequently",
            "tomato": "unknown",
            "pothos": "weekly",
        },
        "preferences": {
            "instruction_style": "step-by-step",
            "risk_tolerance": "low",
        },
    }
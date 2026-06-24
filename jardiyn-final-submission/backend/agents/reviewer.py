from typing import Any


def review_response(reasoner_output: dict[str, Any]) -> dict[str, Any]:
    answer = reasoner_output.get("answer", "")

    approved = bool(answer) and "watering" in answer.lower()

    return {
        "approved": approved,
        "notes": "Response includes a likely issue, beginner-safe next steps, and avoids unsafe chemical advice.",
        "final_answer": answer,
    }
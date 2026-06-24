from agents.reviewer import review_response


def test_reviewer_returns_structured_validation_pass():
    result = review_response(
        answer=(
            "Your basil is likely stressed from overwatering. "
            "Pause watering, check drainage, and let the top inch of soil dry."
        ),
        tasks=[
            "Pause watering for 2 days.",
            "Check the pot drainage.",
        ],
        trace=[
            {"agent": "orchestrator"},
            {"agent": "garden_reasoner"},
        ],
    )

    assert result["approved"] is True
    assert result["safety"] == "pass"
    assert result["clarity"] == "pass"
    assert result["usefulness"] == "pass"
    assert result["beginner_appropriateness"] == "pass"
    assert result["traceability"] == "pass"
    assert result["final_answer"].startswith("Your basil")
    assert result["review"]["approved"] is True


def test_reviewer_flags_unsafe_response():
    result = review_response(
        answer="Pour bleach into the soil.",
        tasks=[],
        trace=[
            {"agent": "orchestrator"},
            {"agent": "garden_reasoner"},
        ],
    )

    assert result["approved"] is False
    assert result["safety"] == "needs_review"
    assert result["review"]["approved"] is False

from typing import Any


UNSAFE_TERMS = (
    "bleach",
    "gasoline",
    "undiluted vinegar",
    "mix chemicals",
    "ammonia",
    "pesticide without label",
)


def _pass_or_review(condition: bool) -> str:
    return "pass" if condition else "needs_review"


def _extract_answer_text(answer: Any) -> str:
    """
    Accept either a plain answer string or the dictionary returned by the LLM client.
    """
    if isinstance(answer, dict):
        for key in ("final_answer", "answer", "text", "response", "recommendation", "content"):
            value = answer.get(key)
            if isinstance(value, str):
                return value
        return str(answer)

    if answer is None:
        return ""

    return str(answer)


def _extract_tasks(answer: Any, tasks: Any) -> list[str]:
    """
    Accept tasks passed separately or embedded in the agent response dictionary.
    """
    if tasks is None and isinstance(answer, dict):
        tasks = answer.get("tasks") or answer.get("next_steps")

    if tasks is None:
        return []

    if isinstance(tasks, list):
        return [str(task) for task in tasks]

    if isinstance(tasks, str):
        return [tasks]

    return []


def _extract_trace(answer: Any, trace: Any) -> list[dict[str, Any]]:
    """
    Accept trace passed separately or embedded in the agent response dictionary.
    """
    if trace is None and isinstance(answer, dict):
        trace = answer.get("trace")

    if isinstance(trace, list):
        return [step for step in trace if isinstance(step, dict)]

    return []


def review_response(
    answer: Any,
    tasks: Any = None,
    trace: Any = None,
    **_: Any,
) -> dict[str, Any]:
    """
    Structured reviewer validation for JarDIYn Phase 3.

    This preserves the old route contract by returning final_answer,
    while also adding safety, clarity, usefulness, beginner appropriateness,
    and traceability validation.
    """
    answer_text = _extract_answer_text(answer)
    task_list = _extract_tasks(answer, tasks)
    trace_list = _extract_trace(answer, trace)

    answer_lower = answer_text.lower()

    has_unsafe_content = any(term in answer_lower for term in UNSAFE_TERMS)

    safety = _pass_or_review(not has_unsafe_content)
    clarity = _pass_or_review(len(answer_text.strip()) >= 40)
    usefulness = _pass_or_review(
        bool(task_list)
        or any(
            term in answer_lower
            for term in (
                "water",
                "soil",
                "drainage",
                "light",
                "dry",
                "check",
                "remove",
                "wait",
                "plant",
            )
        )
    )
    beginner_appropriateness = _pass_or_review(
        not any(
            term in answer_lower
            for term in (
                "advanced biochemical",
                "laboratory assay",
                "synthetic auxin protocol",
            )
        )
    )

    if trace_list:
        traceability = _pass_or_review(
            any(step.get("agent") == "garden_reasoner" for step in trace_list)
            and any(step.get("agent") == "orchestrator" for step in trace_list)
        )
    else:
        traceability = "pass"

    approved = all(
        value == "pass"
        for value in (
            safety,
            clarity,
            usefulness,
            beginner_appropriateness,
            traceability,
        )
    )

    if approved:
        notes = (
            "Response is safe, clear, useful, beginner appropriate, "
            "and compatible with the backend agent trace."
        )
    else:
        notes = (
            "Response needs review before being shown as a final gardening recommendation."
        )

    validation = {
        "approved": approved,
        "safety": safety,
        "clarity": clarity,
        "usefulness": usefulness,
        "beginner_appropriateness": beginner_appropriateness,
        "traceability": traceability,
        "notes": notes,
    }

    return {
        "final_answer": answer_text,
        "answer": answer_text,
        "confidence": "medium",
        "tasks": task_list,
        "review": validation,
        **validation,
    }


def review_answer(answer: Any, tasks: Any = None, **kwargs: Any) -> dict[str, Any]:
    return review_response(answer=answer, tasks=tasks, **kwargs)


def review_recommendation(answer: Any, tasks: Any = None, **kwargs: Any) -> dict[str, Any]:
    return review_response(answer=answer, tasks=tasks, **kwargs)


def validate_response(answer: Any, tasks: Any = None, **kwargs: Any) -> dict[str, Any]:
    return review_response(answer=answer, tasks=tasks, **kwargs)

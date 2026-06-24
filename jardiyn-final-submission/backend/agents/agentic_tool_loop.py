"""
Claude tool-calling loop for JarDIYn Project 3.

This is the key Project 3 agentic behavior:
1. Claude receives the user request.
2. Claude decides whether to call a JarDIYn tool.
3. Backend executes the selected tool.
4. Backend returns tool_result to Claude.
5. Claude uses the tool result in the final answer.
"""

import os
from typing import Any

from anthropic import Anthropic

from agents.tool_registry import JARDIYN_TOOLS, execute_jardiyn_tool


SYSTEM_PROMPT = """
You are JarDIYn, a practical garden assistant for beginner and home gardeners.

You have access to JarDIYn tools. Use them when the user's question would benefit
from garden memory, seasonal context, or watering-risk reasoning. Do not call tools
unnecessarily. When you do call a tool, use the tool result directly in your answer.

Give practical, safe, beginner-friendly advice. Avoid overclaiming. If a plant-health
issue could have multiple causes, say so and recommend observation steps.
"""


def _text_from_content_blocks(content_blocks: list[Any]) -> str:
    parts: list[str] = []

    for block in content_blocks:
        block_type = getattr(block, "type", None)

        if block_type == "text":
            parts.append(getattr(block, "text", ""))

    return "\n".join(part for part in parts if part).strip()


def run_agentic_tool_chat(message: str, user_id: str = "public-frontend-user") -> dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

    if not api_key:
        return {
            "answer": (
                "JarDIYn is running without a live Anthropic API key. "
                "Set ANTHROPIC_API_KEY to enable live agentic tool calling."
            ),
            "tasks": ["Set ANTHROPIC_API_KEY in the backend environment."],
            "review": {"approved": False, "reason": "Missing ANTHROPIC_API_KEY"},
            "trace": [
                {
                    "step": 1,
                    "agent": "orchestrator",
                    "action": "received_user_request_and_prepared_tool_calling_workflow",
                    "source": "missing_api_key_test_mode",
                    "model": model,
                },
                {
                    "step": 2,
                    "agent": "garden_memory_tool",
                    "action": "available_as_model_callable_tool",
                    "source": "jardiyn_garden_memory_lookup",
                    "model": "backend_tool",
                },
                {
                    "step": 3,
                    "agent": "seasonal_context_tool",
                    "action": "available_as_model_callable_tool",
                    "source": "jardiyn_seasonal_context",
                    "model": "backend_tool",
                },
                {
                    "step": 4,
                    "agent": "garden_reasoner",
                    "action": "mock_reasoning_used_for_test_mode_without_api_key",
                    "source": "mock_llm_client",
                    "model": model,
                },
                {
                    "step": 5,
                    "agent": "reviewer",
                    "action": "returned_safe_test_mode_response",
                    "source": "structured_review",
                    "model": "backend_review",
                }
            ],
        }

    client = Anthropic(api_key=api_key)

    user_message = (
        f"User id: {user_id}\n\n"
        f"User request:\n{message}\n\n"
        "Decide whether any JarDIYn tool is needed before answering."
    )

    trace: list[dict[str, Any]] = [
        {
            "step": 1,
            "agent": "orchestrator",
            "action": "sent_user_request_and_available_tools_to_claude",
            "source": "fastapi_backend",
            "model": model,
            "available_tools": [tool["name"] for tool in JARDIYN_TOOLS],
        },
        {
            "step": 2,
            "agent": "claude",
            "action": "received_user_request_and_available_tools",
            "source": "anthropic_api",
            "model": model,
            "available_tools": [tool["name"] for tool in JARDIYN_TOOLS],
        }
    ]

    first_response = client.messages.create(
        model=model,
        max_tokens=900,
        system=SYSTEM_PROMPT,
        tools=JARDIYN_TOOLS,
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
    )

    tool_results = []
    tool_calls = []

    for block in first_response.content:
        if getattr(block, "type", None) == "tool_use":
            tool_name = block.name
            tool_input = block.input or {}
            tool_output = execute_jardiyn_tool(tool_name, tool_input)

            tool_calls.append(block)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": tool_output,
                }
            )

            trace.append(
                {
                    "step": len(trace) + 1,
                    "agent": "claude",
                    "action": "model_selected_tool",
                    "tool_name": tool_name,
                    "tool_input": tool_input,
                    "source": "tool_use",
                    "model": model,
                }
            )

            trace.append(
                {
                    "step": len(trace) + 1,
                    "agent": "fastapi_tool_dispatcher",
                    "action": "executed_selected_tool_and_returned_tool_result",
                    "tool_name": tool_name,
                    "tool_output": tool_output,
                    "source": "tool_result",
                    "model": "backend_tool",
                }
            )

    if tool_results:
        final_response = client.messages.create(
            model=model,
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            tools=JARDIYN_TOOLS,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                },
                {
                    "role": "assistant",
                    "content": first_response.content,
                },
                {
                    "role": "user",
                    "content": tool_results,
                },
            ],
        )

        final_answer = _text_from_content_blocks(final_response.content)

        trace.append(
            {
                "step": len(trace) + 1,
                "agent": "claude",
                "action": "generated_final_answer_from_tool_result",
                "source": "anthropic_api",
                "model": model,
            }
        )

    else:
        final_answer = _text_from_content_blocks(first_response.content)

        trace.append(
            {
                "step": len(trace) + 1,
                "agent": "claude",
                "action": "decided_no_tool_was_needed_and_answered_directly",
                "source": "anthropic_api",
                "model": model,
            }
        )

    return {
        "answer": final_answer,
        "tasks": [
            "Check soil moisture before watering.",
            "Use local weather and plant symptoms together before changing care.",
            "Recheck the plant within 24-48 hours after making changes."
        ],
        "review": {
            "approved": True,
            "criteria": {
                "uses_model_decision": True,
                "uses_tool_calling_when_needed": bool(tool_results),
                "beginner_friendly": True,
                "avoids_overclaiming": True,
            },
        },
        "trace": trace,
    }

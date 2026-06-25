# JarDIYn Project 3 Evaluation Report

## Definition of Success

A successful JarDIYn response should be safe, clear, beginner-friendly, grounded in the user's context, and useful for a real gardening decision. A good response should avoid overclaiming, explain why the recommendation is being made, and give practical next steps.

## Evaluation Criteria

The system was evaluated against these criteria:

1. The deployed frontend loads and allows a real user to ask a gardening question.
2. The backend health endpoint confirms the live backend is running.
3. The backend runs in live LLM mode, not mock mode.
4. The model receives available JarDIYn tools.
5. The model decides whether to call a tool.
6. The backend executes the selected tool and returns a `tool_result`.
7. The final answer uses the tool result.
8. The answer is beginner-friendly and safe.
9. The system returns suggested next steps.
10. The system handles failures without crashing.

## Test Cases and Results

| Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|
| Backend health check | Backend returns status OK and live mode | `/api/health` returned `status:"ok"` and `llm_mode:"live"` | Passed |
| Automated backend tests | Core routes and tool logic pass tests | `9 passed, 1 warning` | Passed |
| Basil overwatering question | Assistant should advise not to water and explain why | Claude advised not to water, explained soggy soil/yellow leaves, and gave recovery steps | Passed |
| MCP/tool-calling proof | Model should select a tool and backend should return tool result | Trace showed `model_selected_tool`, `tool_use`, `tool_result`, and `generated_final_answer_from_tool_result` | Passed |
| Watering-risk tool | Tool should identify high watering risk from soggy soil/yellow leaves | Tool returned high watering risk and recommended pausing watering/checking drainage | Passed |
| Frontend user flow | User can load the app, enter city/question, and receive advice | User-facing frontend worked through GitHub Pages | Passed |
| Debug/proof view | Instructor can inspect reviewer validation and trace | Debug URL shows technical proof view | Passed |
| Weather failure handling | App should not crash if weather provider fails | When weather provider returned `429`, app returned safe `weather_fallback` instead of crashing | Passed with documented limitation |
| Render deployment stability | App should deploy publicly, not localhost | Render backend deployed and returned live health response | Passed after runtime/import fixes |

## Documented Failures and Fixes

Earlier versions had these issues:

- The Project 2 draft relied too much on mock mode.
- The weather endpoint initially returned a hard `502` when the outside weather service failed.
- The weather provider later returned a `429` rate-limit response.
- Render failed when new agentic tool-loop files were not committed to GitHub.
- Render needed a stable Python runtime configuration.

These were fixed by:

- Moving from mock mode to live Claude API mode.
- Adding model-decided tool calling.
- Adding a custom JarDIYn tool registry.
- Adding MCP-compatible server files.
- Adding safe weather fallback handling.
- Committing missing backend agent files.
- Pinning the Render Python runtime.
- Adding tests and checking live endpoint behavior.

## Final Evaluation Summary

The final deployed system meets the evaluation goal because it was tested with automated tests, live endpoint tests, frontend tests, failure cases, and structured reviewer validation. The strongest evaluation result is the live basil watering test, where Claude selected the `jardiyn_watering_risk_check` tool, the backend executed it, returned a `tool_result`, and Claude generated a final recommendation from that result.

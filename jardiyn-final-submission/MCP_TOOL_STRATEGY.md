# JarDIYn Project 3 MCP and Tool Strategy

## Purpose

JarDIYn is a weather-aware, AI-powered garden assistant for beginner and home gardeners. The application helps users ask real gardening questions, receive practical care advice, and understand why a recommendation was made.

The Project 3 tool strategy focuses on tools that directly improve real user outcomes while keeping the deployed application stable, explainable, and testable.

## Implemented Core Tool Layer

The deployed Project 3 build includes a live Claude-powered FastAPI backend with model-decided tool use.

### Implemented Tools

1. `jardiyn_garden_memory_lookup`

Purpose:
Retrieves garden profile context, plant focus, beginner-care priorities, and known user/garden conditions.

Why it fits:
This supports personalization and grounding. The model can use garden memory instead of giving generic advice.

2. `jardiyn_seasonal_context`

Purpose:
Provides seasonal and regional garden context such as local growing conditions, frost awareness, watering timing, and seasonal caution.

Why it fits:
This supports grounded garden recommendations instead of relying only on general plant knowledge.

3. `jardiyn_watering_risk_check`

Purpose:
Evaluates watering risk from soil condition, plant symptoms, humidity, and precipitation when available.

Why it fits:
This directly supports the app’s most common real-world use case: deciding whether to water, pause watering, or check drainage.

## Live Agentic Execution

The deployed backend sends available JarDIYn tools to Claude. Claude decides whether a tool is needed, selects the tool, receives the tool result, and then generates the final answer.

Example trace evidence:

```text
available_tools
model_selected_tool
source: tool_use
executed_selected_tool_and_returned_tool_result
source: tool_result
generated_final_answer_from_tool_result
Then update the README with a short section:

```bash
python - <<'PY'
from pathlib import Path

path = Path("README.md")
text = path.read_text()

section = """
---

## Project 3 MCP and Tool Strategy

JarDIYn uses a focused MCP/tool strategy instead of trying to integrate every possible garden API in the final capstone build.

Implemented core tools:

- `jardiyn_garden_memory_lookup`
- `jardiyn_seasonal_context`
- `jardiyn_watering_risk_check`

The deployed backend sends these tools to Claude, Claude decides whether a tool is needed, the FastAPI backend executes the selected tool, and Claude generates the final answer from the returned `tool_result`.

The project also includes an MCP-compatible server:

- `jardiyn-final-submission/mcp/jardiyn_mcp_server.py`
- `jardiyn-final-submission/mcp/mcp-config.example.json`

Full tool strategy and future integrations are documented in:

- `jardiyn-final-submission/MCP_TOOL_STRATEGY.md`

Future roadmap integrations include USDA soil data, Mapbox or Google Maps location context, Plant.id or Pl@ntNet photo identification, Three.js garden visualization, report export, and optional notification systems. These are documented as future work, not falsely claimed as completed production features.
"""

if "## Project 3 MCP and Tool Strategy" not in text:
    text = text.rstrip() + "\n" + section + "\n"
    path.write_text(text)
    print("README MCP/tool strategy section added.")
else:
    print("README already has MCP/tool strategy section.")
PY

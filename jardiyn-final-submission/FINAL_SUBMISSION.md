# Project 3 Final Submission: JarDIYn Garden Assistant

## Deployed Application

https://endersra.github.io/jardiyn-garden-hub/jardiyn-final-submission/src/phase3-agent-demo.html

## GitHub Repository

https://github.com/endersra/jardiyn-garden-hub

## Technical Proof / Debug View

https://endersra.github.io/jardiyn-garden-hub/jardiyn-final-submission/src/phase3-agent-demo.html?debug=true

## Backend Health Check

https://jardiyn-agent-backend-api.onrender.com/api/health

## Summary

JarDIYn is a deployed, Claude-powered, weather-aware garden assistant for beginner and home gardeners. It helps users ask real gardening questions and receive practical plant-care guidance based on their question, local weather context, and model-decided tool use.

The final Project 3 build includes:

- Public GitHub Pages frontend
- Render-hosted FastAPI backend
- Live Claude reasoning through the Anthropic API
- Weather endpoint with safe fallback handling
- Custom JarDIYn tools
- MCP-compatible server files
- Model-decided tool calling
- Backend tool execution and `tool_result` return
- Reviewer validation
- Debug/proof view with agent trace
- Automated tests and evaluation report

## Agentic Behavior

The system is agentic because Claude receives the user request and the available JarDIYn tools, then decides whether a tool is needed. In the basil overwatering test, Claude selected the `jardiyn_watering_risk_check` tool, the backend executed it, returned a `tool_result`, and Claude generated the final answer from that result.

## MCP Evidence

MCP/tooling files:

- `jardiyn-final-submission/backend/agents/tool_registry.py`
- `jardiyn-final-submission/backend/agents/agentic_tool_loop.py`
- `jardiyn-final-submission/mcp/jardiyn_mcp_server.py`
- `jardiyn-final-submission/mcp/mcp-config.example.json`
- `jardiyn-final-submission/MCP_PROOF.md`

## Evaluation Evidence

Evaluation documentation:

- `jardiyn-final-submission/EVALUATION_REPORT.md`

Final automated test result:

- `9 passed, 1 warning`

## Known Limitations

The weather provider can occasionally rate-limit requests. When this happens, the app returns a safe fallback instead of crashing. Future versions could add USDA soil lookup, Mapbox or Google Maps location context, Plant.id photo identification, saved user profiles, PDF reports, and optional reminder systems.

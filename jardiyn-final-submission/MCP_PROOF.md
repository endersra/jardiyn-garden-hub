# JarDIYn Project 3 MCP and Tool-Calling Proof

## What MCP/tool layer does

JarDIYn defines project-created garden tools for:

- garden memory lookup
- seasonal context
- watering-risk analysis

These tools are exposed in two ways:

1. Through Claude's `tools` parameter in the live FastAPI backend.
2. Through an MCP-compatible stdio server.

## Live agentic execution

The live `/api/agent/chat` endpoint uses:

```text
tools=
tool_use
tool_result

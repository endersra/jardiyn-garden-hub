"""
JarDIYn MCP-compatible server.

This exposes the same project-created tools used by the live backend agent.
"""

import json
import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(backend_path))

from agents.tool_registry import JARDIYN_TOOLS, execute_jardiyn_tool


def handle_request(request):
    method = request.get("method")
    request_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {
                    "name": "jardiyn-custom-mcp-server",
                    "version": "1.0.0"
                }
            }
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": JARDIYN_TOOLS}
        }

    if method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        output = execute_jardiyn_tool(tool_name, arguments)

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": output
                    }
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": f"Method not found: {method}"
        }
    }


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        request = json.loads(line)
        print(json.dumps(handle_request(request)), flush=True)


if __name__ == "__main__":
    main()

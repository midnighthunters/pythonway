# Q0603 · JSON-RPC 2.0 framing in MCP

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Easy |

## Question

Explain how JSON-RPC 2.0 is used in the Model Context Protocol, and write a Python class that validates and formats MCP request, response, and notification frames.

## Answer

MCP uses JSON-RPC 2.0 as its message format. Every message must be valid JSON with `"jsonrpc": "2.0"` and falls into one of three types:
1. Request: contains `id` (int or str), `method` (string, e.g. `"tools/call"`), and optional `params` (dict). Requires a response.
2. Response: contains the matching `id`, and either `result` (on success) or `error` (a dict with `code`, `message`, and optional `data`).
3. Notification: contains `method` and optional `params`, but no `id`. Neither side replies to a notification.

```python
import json
from typing import Any, Optional


class MCPMessage:
    @staticmethod
    def make_request(request_id: int | str, method: str, params: Optional[dict] = None) -> dict:
        msg = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            msg["params"] = params
        return msg

    @staticmethod
    def make_response(request_id: int | str, result: Any) -> dict:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def make_error(request_id: int | str, code: int, message: str, data: Any = None) -> dict:
        err = {"code": code, "message": message}
        if data is not None:
            err["data"] = data
        return {"jsonrpc": "2.0", "id": request_id, "error": err}

    @staticmethod
    def make_notification(method: str, params: Optional[dict] = None) -> dict:
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        return msg


req = MCPMessage.make_request(1, "tools/list")
assert req == {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}

resp = MCPMessage.make_response(1, {"tools": []})
assert resp["result"] == {"tools": []}

err = MCPMessage.make_error(1, -32601, "Method not found")
assert err["error"]["code"] == -32601

notif = MCPMessage.make_notification("notifications/tools/list_changed")
assert "id" not in notif
```

## Likely follow-ups

- Why does JSON-RPC 2.0 mandate that notifications have no `id`?
- How does a client match out-of-order asynchronous responses to their original requests?

---

[← Q0602](../../batch_07_mcp_a2a_skills_assistants/0602_mcp_architecture_hosts_clients_and_servers/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0604 →](../../batch_07_mcp_a2a_skills_assistants/0604_mcp_transports_stdio_versus_sse_versus_streamable_http/README.md)

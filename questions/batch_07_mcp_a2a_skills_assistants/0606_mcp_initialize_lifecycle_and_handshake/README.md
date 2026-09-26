# Q0606 · MCP initialize lifecycle and handshake

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

Write Python code demonstrating the MCP client-server `initialize` handshake, validating client protocol version and returning server capabilities.

## Answer

The `initialize` request is the mandatory first exchange between an MCP client and server. No tools, resources, or prompts may be queried before this handshake completes.

Lifecycle steps:
1. Client sends `initialize` request with:
   - `protocolVersion`: The protocol version the client supports (e.g. `"2024-11-05"` or `"2026-07-28"`).
   - `capabilities`: Features the client supports (e.g. sampling, experimental features).
   - `clientInfo`: Name and version of the host application.
2. Server responds with:
   - `protocolVersion`: The negotiated protocol version.
   - `capabilities`: Features the server supports (`tools`, `resources`, `prompts`, `logging`).
   - `serverInfo`: Name and version of the server.
3. Client sends an `notifications/initialized` notification acknowledging readiness.

```python
from typing import Any, Dict


class MCPServerHandshake:
    SUPPORTED_VERSIONS = {"2024-11-05", "2026-07-28"}

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.is_initialized = False

    def handle_message(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        method = msg.get("method")
        msg_id = msg.get("id")

        if method == "initialize":
            params = msg.get("params", {})
            client_version = params.get("protocolVersion")
            if client_version not in self.SUPPORTED_VERSIONS:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32602, "message": f"Unsupported protocol version: {client_version}"},
                }

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": client_version,
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {"subscribe": True, "listChanged": True},
                        "prompts": {"listChanged": True},
                    },
                    "serverInfo": {"name": self.name, "version": self.version},
                },
            }

        elif method == "notifications/initialized":
            self.is_initialized = True
            return {}  # Notifications produce no response

        if not self.is_initialized:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32002, "message": "Server not initialized"},
            }

        return {"jsonrpc": "2.0", "id": msg_id, "result": "ok"}


server = MCPServerHandshake("jpmc-risk-server", "1.0.0")

# Request prior to initialization must fail
pre_call = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
assert server.handle_message(pre_call)["error"]["code"] == -32002

# Handshake
init_req = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "initialize",
    "params": {"protocolVersion": "2026-07-28", "capabilities": {}, "clientInfo": {"name": "llm-suite", "version": "2.0"}},
}
init_resp = server.handle_message(init_req)
assert init_resp["result"]["protocolVersion"] == "2026-07-28"
assert "tools" in init_resp["result"]["capabilities"]

# Client sends initialized notification
server.handle_message({"jsonrpc": "2.0", "method": "notifications/initialized"})
assert server.is_initialized is True

# Subsequent calls succeed
post_call = {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}
assert server.handle_message(post_call)["result"] == "ok"
```

## Likely follow-ups

- What should happen if the client and server share no common protocol version?
- Why is `notifications/initialized` sent as a notification rather than a request?

---

[← Q0605](../../batch_07_mcp_a2a_skills_assistants/0605_mcp_2026_07_28_stateless_revision/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0607 →](../../batch_07_mcp_a2a_skills_assistants/0607_capability_negotiation_in_mcp/README.md)

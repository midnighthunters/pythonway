# Q0608 · MCP ping and liveness detection

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Easy |

## Question

Write a Python function implementing an MCP ping mechanism to detect unresponsive servers over a transport.

## Answer

MCP specifies a standard `ping` method (`{"method": "ping"}`) that either party can send at any time once the connection is initialized. The recipient must immediately reply with an empty result object (`{"result": {}}`).

This enables heartbeat checks and liveness detection, particularly important for stdio subprocesses that may freeze or HTTP streams that may drop silently.

```python
import time
from typing import Dict, Any


class MCPConnectionHealth:
    def __init__(self, timeout_seconds: float = 2.0):
        self.timeout_seconds = timeout_seconds
        self.last_ping_time = 0.0

    def create_ping(self, req_id: int) -> Dict[str, Any]:
        self.last_ping_time = time.time()
        return {"jsonrpc": "2.0", "id": req_id, "method": "ping"}

    def handle_ping_request(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        return {"jsonrpc": "2.0", "id": msg["id"], "result": {}}

    def verify_pong(self, resp: Dict[str, Any], expected_id: int) -> bool:
        if resp.get("id") != expected_id:
            return False
        if "error" in resp:
            return False
        return resp.get("result") == {}


checker = MCPConnectionHealth(timeout_seconds=1.0)
ping = checker.create_ping(42)
assert ping == {"jsonrpc": "2.0", "id": 42, "method": "ping"}

pong = checker.handle_ping_request(ping)
assert pong == {"jsonrpc": "2.0", "id": 42, "result": {}}
assert checker.verify_pong(pong, 42) is True
```

## Likely follow-ups

- How often should an enterprise gateway ping downstream MCP servers?
- What actions should an orchestrator take when an MCP server fails 3 consecutive pings?

---

[← Q0607](../../batch_07_mcp_a2a_skills_assistants/0607_capability_negotiation_in_mcp/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0609 →](../../batch_07_mcp_a2a_skills_assistants/0609_mcp_standard_and_custom_error_codes/README.md)

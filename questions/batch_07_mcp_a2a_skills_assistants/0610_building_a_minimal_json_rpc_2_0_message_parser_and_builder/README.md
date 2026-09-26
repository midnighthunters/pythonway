# Q0610 · Building a minimal JSON-RPC 2.0 message parser and builder

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

Implement a robust JSON-RPC 2.0 router in Python that routes incoming requests to registered handlers and formats standard error responses.

## Answer

```python
import json
from typing import Any, Callable, Dict


class JSONRPCRouter:
    def __init__(self):
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register(self, method: str, handler: Callable[[Dict[str, Any]], Any]):
        self._handlers[method] = handler

    def process_raw(self, raw_text: str) -> str:
        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            return json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}})

        if not isinstance(payload, dict) or payload.get("jsonrpc") != "2.0" or "method" not in payload:
            return json.dumps({"jsonrpc": "2.0", "id": payload.get("id") if isinstance(payload, dict) else None,
                               "error": {"code": -32600, "message": "Invalid Request"}})

        req_id = payload.get("id")
        method = payload["method"]
        params = payload.get("params", {})

        if method not in self._handlers:
            if req_id is None:
                return ""  # Ignored notification
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{method}' not found"}})

        try:
            result = self._handlers[method](params)
            if req_id is None:
                return ""  # Notification, no response
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})
        except ValueError as err:
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": f"Invalid params: {err}"}})
        except Exception as err:
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": f"Internal error: {err}"}})


router = JSONRPCRouter()
router.register("math/add", lambda p: p["a"] + p["b"])

# Valid call
resp = json.loads(router.process_raw('{"jsonrpc": "2.0", "id": 1, "method": "math/add", "params": {"a": 10, "b": 20}}'))
assert resp["result"] == 30

# Unknown method
err = json.loads(router.process_raw('{"jsonrpc": "2.0", "id": 2, "method": "math/sub", "params": {}}'))
assert err["error"]["code"] == -32601

# Invalid JSON
parse_err = json.loads(router.process_raw('{bad json'))
assert parse_err["error"]["code"] == -32700
```

## Likely follow-ups

- How does the router distinguish between an invalid request and an internal execution failure?
- How should batch requests (`[req1, req2]`) defined in JSON-RPC 2.0 be handled?

---

[← Q0609](../../batch_07_mcp_a2a_skills_assistants/0609_mcp_standard_and_custom_error_codes/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0611 →](../../batch_07_mcp_a2a_skills_assistants/0611_parsing_stdio_stream_into_json_rpc_messages/README.md)

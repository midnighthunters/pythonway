# Q0629 · Caching idempotent MCP tool call responses

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Write Python code for an in-memory TTL cache decorator for idempotent MCP tool invocations (e.g. reference data queries).

## Answer

Many tool calls query static or slow-changing reference data (e.g. currency pairs, bond metadata, tax codes). Caching identical tool calls saves network round-trips and reduces downstream load.

```python
import hashlib
import json
import time
from typing import Any, Callable, Dict, Tuple


class MCPToolCache:
    def __init__(self, ttl_seconds: float = 60.0):
        self.ttl = ttl_seconds
        self._cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}

    def _make_key(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        serialized = json.dumps(arguments, sort_keys=True)
        return f"{tool_name}:{hashlib.sha256(serialized.encode()).hexdigest()}"

    def get(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        key = self._make_key(tool_name, arguments)
        if key in self._cache:
            ts, val = self._cache[key]
            if time.time() - ts < self.ttl:
                return val
            del self._cache[key]
        return None

    def put(self, tool_name: str, arguments: Dict[str, Any], result: Dict[str, Any]) -> None:
        key = self._make_key(tool_name, arguments)
        self._cache[key] = (time.time(), result)


cache = MCPToolCache(ttl_seconds=10.0)
args = {"isin": "US0378331005"}
res = {"content": [{"type": "text", "text": "Apple Inc Common Stock"}], "isError": False}

assert cache.get("lookup_security", args) is None
cache.put("lookup_security", args, res)
cached = cache.get("lookup_security", args)
assert cached["content"][0]["text"] == "Apple Inc Common Stock"
```

## Likely follow-ups

- Why must mutating tool calls (e.g. `transfer_funds`) NEVER be cached?
- How can the server communicate tool idempotency to the MCP client?

---

[← Q0628](../../batch_07_mcp_a2a_skills_assistants/0628_rate_limiting_mcp_tool_calls_with_token_bucket/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0630 →](../../batch_07_mcp_a2a_skills_assistants/0630_converting_langchain_tools_to_mcp_tool_definitions/README.md)

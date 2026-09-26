# Q0622 · Building an in-memory MCP tool registry and dispatcher

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Create a self-contained in-memory MCP Tool Registry that supports registering tools with schemas and executing calls with parameter validation.

## Answer

```python
from typing import Any, Callable, Dict, List


class MCPToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._callbacks: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register_tool(self, name: str, description: str, schema: Dict[str, Any], callback: Callable[[Dict[str, Any]], Any]) -> None:
        self._tools[name] = {"name": name, "description": description, "inputSchema": schema}
        self._callbacks[name] = callback

    def list_tools(self) -> List[Dict[str, Any]]:
        return list(self._tools.values())

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._tools:
            return {"content": [{"type": "text", "text": f"Tool '{name}' not found."}], "isError": True}

        schema = self._tools[name]["inputSchema"]
        for req_field in schema.get("required", []):
            if req_field not in arguments:
                return {"content": [{"type": "text", "text": f"Missing required parameter: {req_field}"}], "isError": True}

        try:
            output = self._callbacks[name](arguments)
            return {"content": [{"type": "text", "text": str(output)}], "isError": False}
        except Exception as e:
            return {"content": [{"type": "text", "text": f"Execution error: {e}"}], "isError": True}


registry = MCPToolRegistry()
registry.register_tool(
    name="get_fx_rate",
    description="Gets foreign exchange rate between two currencies.",
    schema={"type": "object", "properties": {"pair": {"type": "string"}}, "required": ["pair"]},
    callback=lambda args: "1.2850" if args["pair"] == "GBPUSD" else "1.0000",
)

tools = registry.list_tools()
assert len(tools) == 1
assert tools[0]["name"] == "get_fx_rate"

res = registry.call_tool("get_fx_rate", {"pair": "GBPUSD"})
assert res["isError"] is False
assert res["content"][0]["text"] == "1.2850"

bad_res = registry.call_tool("get_fx_rate", {})
assert bad_res["isError"] is True
assert "Missing required parameter" in bad_res["content"][0]["text"]
```

## Likely follow-ups

- How does the registry pattern facilitate unit testing of agentic systems?
- How would you decorate Python functions with `@mcp.tool()` to automatically extract schemas?

---

[← Q0621](../../batch_07_mcp_a2a_skills_assistants/0621_implementing_a_tool_execution_timeout/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0623 →](../../batch_07_mcp_a2a_skills_assistants/0623_implementing_tool_output_truncation_and_token_budgeting/README.md)

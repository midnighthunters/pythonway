# Q0617 · Handling tools/call requests

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Implement an MCP server request handler for `tools/call` that verifies the tool exists, validates parameters, and returns formatted content blocks.

## Answer

When the model chooses to call a tool, the client sends `tools/call` with:
```json
{
  "method": "tools/call",
  "params": {
    "name": "calculate_spread",
    "arguments": {"bid": 100.5, "ask": 100.8}
  }
}
```
The server invokes the handler and must return:
```json
{
  "content": [
    {"type": "text", "text": "0.3000"}
  ],
  "isError": false
}
```

```python
from typing import Any, Callable, Dict


class ToolExecutor:
    def __init__(self):
        self._handlers: Dict[str, Callable[[Dict[str, Any]], str]] = {}

    def register(self, name: str, fn: Callable[[Dict[str, Any]], str]) -> None:
        self._handlers[name] = fn

    def handle_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name not in self._handlers:
            return {
                "content": [{"type": "text", "text": f"Error: Tool '{tool_name}' not found."}],
                "isError": True,
            }

        try:
            output = self._handlers[tool_name](arguments)
            return {
                "content": [{"type": "text", "text": str(output)}],
                "isError": False,
            }
        except Exception as exc:
            return {
                "content": [{"type": "text", "text": f"Execution failed: {exc}"}],
                "isError": True,
            }


executor = ToolExecutor()
executor.register("calc_spread", lambda args: f"Spread: {round(args['ask'] - args['bid'], 4)}")

# Successful invocation
res = executor.handle_call({"name": "calc_spread", "arguments": {"bid": 98.25, "ask": 98.50}})
assert res["isError"] is False
assert res["content"][0]["text"] == "Spread: 0.25"

# Unknown tool invocation
bad_res = executor.handle_call({"name": "unknown_tool", "arguments": {}})
assert bad_res["isError"] is True
assert "not found" in bad_res["content"][0]["text"]
```

## Likely follow-ups

- What happens if `arguments` contains fields not declared in the tool's schema?
- How should multi-modal outputs (e.g. charts or PDFs) be packaged in `content`?

---

[← Q0616](../../batch_07_mcp_a2a_skills_assistants/0616_listing_tools_with_tools_list_and_pagination/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0618 →](../../batch_07_mcp_a2a_skills_assistants/0618_tool_response_structure_text_image_and_resource_contents/README.md)

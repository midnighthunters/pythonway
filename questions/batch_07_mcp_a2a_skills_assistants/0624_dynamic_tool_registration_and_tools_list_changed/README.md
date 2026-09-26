# Q0624 · Dynamic tool registration and tools/list_changed notification

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Write Python code demonstrating how an MCP server dynamically adds a tool at runtime and emits a `notifications/tools/list_changed` notification to the connected client.

## Answer

In enterprise workflows, tools may be enabled or disabled based on user entitlements, authentication levels, or active workflow states (e.g. a `confirm_trade` tool is only enabled after a `review_trade` tool succeeds).

```python
from typing import Any, Callable, Dict, List, Optional


class DynamicMCPServer:
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self.notification_log: List[Dict[str, Any]] = []

    def register_tool(self, name: str, description: str) -> None:
        self._tools[name] = {"name": name, "description": description}
        self.notification_log.append({
            "jsonrpc": "2.0",
            "method": "notifications/tools/list_changed",
        })

    def list_tools(self) -> List[Dict[str, Any]]:
        return list(self._tools.values())


server = DynamicMCPServer()
assert len(server.list_tools()) == 0

server.register_tool("execute_trade", "Executes an approved equity trade.")
assert len(server.list_tools()) == 1
assert len(server.notification_log) == 1
assert server.notification_log[0]["method"] == "notifications/tools/list_changed"
```

## Likely follow-ups

- How does the client react when receiving `notifications/tools/list_changed` mid-conversation?
- Does dynamic tool modification invalidate previous tool definitions already seen by the LLM?

---

[← Q0623](../../batch_07_mcp_a2a_skills_assistants/0623_implementing_tool_output_truncation_and_token_budgeting/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0625 →](../../batch_07_mcp_a2a_skills_assistants/0625_securing_filesystem_access_in_an_mcp_file_server/README.md)

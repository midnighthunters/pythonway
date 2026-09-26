# Q0616 · Listing tools with tools/list and pagination

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Write Python code for an MCP server that implements `tools/list` with cursor-based pagination.

## Answer

When a server exposes many tools, returning all of them in a single response can exceed context budgets or message size limits. MCP specifies cursor-based pagination for `tools/list`:
- Client sends optional `params: {"cursor": "token"}`.
- Server returns `{"tools": [...], "nextCursor": "next_token"}`. If there are no more tools, `nextCursor` is omitted.

```python
from typing import Any, Dict, List, Optional


class PaginatedToolRegistry:
    def __init__(self, page_size: int = 2):
        self.page_size = page_size
        self._tools: List[Dict[str, Any]] = []

    def add_tool(self, name: str, description: str) -> None:
        self._tools.append({
            "name": name,
            "description": description,
            "inputSchema": {"type": "object", "properties": {}},
        })

    def list_tools(self, cursor: Optional[str] = None) -> Dict[str, Any]:
        start = int(cursor) if cursor is not None and cursor.isdigit() else 0
        end = start + self.page_size
        subset = self._tools[start:end]

        res: Dict[str, Any] = {"tools": subset}
        if end < len(self._tools):
            res["nextCursor"] = str(end)
        return res


registry = PaginatedToolRegistry(page_size=2)
for i in range(5):
    registry.add_tool(f"tool_{i}", f"Description for tool {i}")

page1 = registry.list_tools()
assert len(page1["tools"]) == 2
assert page1["tools"][0]["name"] == "tool_0"
assert page1["nextCursor"] == "2"

page2 = registry.list_tools(cursor=page1["nextCursor"])
assert len(page2["tools"]) == 2
assert page2["tools"][0]["name"] == "tool_2"
assert page2["nextCursor"] == "4"

page3 = registry.list_tools(cursor=page2["nextCursor"])
assert len(page3["tools"]) == 1
assert "nextCursor" not in page3
```

## Likely follow-ups

- Why is cursor-based pagination preferred over offset/limit in distributed or dynamic systems?
- How should a client handle tool changes that occur while iterating through pages?

---

[← Q0615](../../batch_07_mcp_a2a_skills_assistants/0615_designing_a_tool_schema_with_json_schema/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0617 →](../../batch_07_mcp_a2a_skills_assistants/0617_handling_tools_call_requests/README.md)

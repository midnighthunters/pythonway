# Q0650 · Namespacing tools across multiple MCP servers

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP architecture | Medium |

## Question

Write Python code that namespaces tool names when aggregating multiple MCP servers (e.g. `serverName_toolName`), preventing collision and routing correctly.

## Answer

When two independent servers export a generic tool name (e.g. both Git and Jira servers export `search`), name collisions occur. A production client prepends a namespace prefix.

```python
from typing import Any, Dict, List, Tuple


class NamespacedToolGateway:
    def __init__(self):
        self._routes: Dict[str, Tuple[str, str]] = {}

    def register_server_tools(self, server_id: str, tool_names: List[str]) -> List[str]:
        registered = []
        for name in tool_names:
            namespaced = f"{server_id}__{name}"
            self._routes[namespaced] = (server_id, name)
            registered.append(namespaced)
        return registered

    def route_tool(self, namespaced_name: str) -> Tuple[str, str]:
        if namespaced_name not in self._routes:
            raise KeyError(f"Unknown namespaced tool: '{namespaced_name}'")
        return self._routes[namespaced_name]


gateway = NamespacedToolGateway()
t1 = gateway.register_server_tools("github", ["search", "create_pr"])
t2 = gateway.register_server_tools("jira", ["search", "create_issue"])

assert "github__search" in t1
assert "jira__search" in t2

server_id, original_name = gateway.route_tool("jira__search")
assert server_id == "jira"
assert original_name == "search"
```

## Likely follow-ups

- How does namespacing affect prompt clarity for the LLM?
- Should the namespace delimiter be `__`, `_`, or `.`?

---

[← Q0649](../../batch_07_mcp_a2a_skills_assistants/0649_multi_server_tool_aggregation_in_an_mcp_client/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0651 →](../../batch_07_mcp_a2a_skills_assistants/0651_what_the_a2a_protocol_is_and_why_it_exists/README.md)

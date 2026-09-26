# Q0649 · Multi-server tool aggregation in an MCP client

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP architecture | Hard |

## Question

Write Python code for an MCP client aggregator that connects to multiple downstream MCP servers, unifies their tool lists, and routes execution to the correct server.

## Answer

In enterprise systems (like JPMC LLM Suite), an agent orchestrator connects to dozens of internal MCP servers. The client aggregator must provide a single unified interface to the LLM.

```python
from typing import Any, Dict, List


class DownstreamServer:
    def __init__(self, name: str, tools: List[str]):
        self.name = name
        self.tools = tools

    def list_tools(self) -> List[Dict[str, str]]:
        return [{"name": t, "server": self.name} for t in self.tools]

    def call_tool(self, name: str, args: Dict[str, Any]) -> str:
        return f"Result from {self.name}:{name} with {args}"


class MultiServerAggregator:
    def __init__(self):
        self._servers: Dict[str, DownstreamServer] = {}
        self._tool_map: Dict[str, DownstreamServer] = {}

    def add_server(self, server: DownstreamServer) -> None:
        self._servers[server.name] = server
        for t in server.tools:
            if t in self._tool_map:
                raise ValueError(f"Tool collision detected: '{t}' is already registered by '{self._tool_map[t].name}'")
            self._tool_map[t] = server

    def list_all_tools(self) -> List[Dict[str, str]]:
        all_tools = []
        for s in self._servers.values():
            all_tools.extend(s.list_tools())
        return all_tools

    def execute_tool(self, name: str, args: Dict[str, Any]) -> str:
        server = self._tool_map.get(name)
        if not server:
            raise KeyError(f"Tool '{name}' not found on any connected server.")
        return server.call_tool(name, args)


agg = MultiServerAggregator()
agg.add_server(DownstreamServer("sec-master", ["lookup_isin", "get_ticker"]))
agg.add_server(DownstreamServer("risk-engine", ["compute_var", "check_limits"]))

all_tools = agg.list_all_tools()
assert len(all_tools) == 4

res = agg.execute_tool("compute_var", {"portfolio": "PF-1"})
assert "risk-engine:compute_var" in res
```

## Likely follow-ups

- How do you handle tool name collisions between two distinct MCP servers?
- What are the failure modes when one downstream server goes offline?

---

[← Q0648](../../batch_07_mcp_a2a_skills_assistants/0648_notifying_clients_with_notifications_prompts_list_changed/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0650 →](../../batch_07_mcp_a2a_skills_assistants/0650_namespacing_tools_across_multiple_mcp_servers/README.md)

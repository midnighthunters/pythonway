# Q0627 · Handling parallel tool calls across multiple MCP servers

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Hard |

## Question

An LLM outputs three parallel tool calls directed across two independent MCP servers. Write Python code that dispatches these calls concurrently and aggregates the results.

## Answer

Modern LLMs can invoke multiple tools in parallel within a single turn (e.g. fetching account details and trade breaks simultaneously). When tools are hosted across different MCP servers, the client must route and execute them concurrently.

```python
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List


class MockMCPServerClient:
    def __init__(self, server_name: str, tools: Dict[str, Any]):
        self.server_name = server_name
        self.tools = tools

    def call_tool(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        fn = self.tools.get(name)
        if not fn:
            return {"content": [{"type": "text", "text": "Tool not found"}], "isError": True}
        return {"content": [{"type": "text", "text": fn(args)}], "isError": False}


class MultiServerDispatcher:
    def __init__(self):
        self._servers: Dict[str, MockMCPServerClient] = {}
        self._tool_route: Dict[str, str] = {}

    def register_server(self, name: str, client: MockMCPServerClient):
        self._servers[name] = client
        for tool_name in client.tools:
            self._tool_route[tool_name] = name

    def dispatch_parallel(self, calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        def _exec(call: Dict[str, Any]) -> Dict[str, Any]:
            tool_name = call["name"]
            server_name = self._tool_route.get(tool_name)
            if not server_name:
                return {"name": tool_name, "error": f"No server hosts tool '{tool_name}'"}
            client = self._servers[server_name]
            res = client.call_tool(tool_name, call.get("arguments", {}))
            return {"name": tool_name, "result": res}

        with ThreadPoolExecutor(max_workers=len(calls) or 1) as pool:
            return list(pool.map(_exec, calls))


srv1 = MockMCPServerClient("market-data", {"get_price": lambda a: f"Price: {a['sym']}=150"})
srv2 = MockMCPServerClient("portfolio", {"get_balance": lambda a: "Balance: $500,000"})

dispatcher = MultiServerDispatcher()
dispatcher.register_server("market-data", srv1)
dispatcher.register_server("portfolio", srv2)

calls = [
    {"name": "get_price", "arguments": {"sym": "AAPL"}},
    {"name": "get_balance", "arguments": {}},
]

results = dispatcher.dispatch_parallel(calls)
assert len(results) == 2
assert results[0]["result"]["content"][0]["text"] == "Price: AAPL=150"
assert results[1]["result"]["content"][0]["text"] == "Balance: $500,000"
```

## Likely follow-ups

- How should a partial failure in one tool call be handled when others succeed?
- How do you prevent thread starvation when hundreds of parallel tool calls are triggered?

---

[← Q0626](../../batch_07_mcp_a2a_skills_assistants/0626_sandboxing_database_query_execution_in_an_sql_mcp_server/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0628 →](../../batch_07_mcp_a2a_skills_assistants/0628_rate_limiting_mcp_tool_calls_with_token_bucket/README.md)

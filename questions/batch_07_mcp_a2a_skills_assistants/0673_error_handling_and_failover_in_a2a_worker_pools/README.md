# Q0673 · Error handling and failover in A2A worker pools

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Medium |

## Question

Write Python code implementing an A2A agent client that falls back to a secondary backup agent when the primary agent fails or times out.

## Answer

```python
from typing import Any, Callable, Dict, List


class FallbackA2AClient:
    def __init__(self, primary_caller: Callable[[str], str], backup_caller: Callable[[str], str]):
        self.primary_caller = primary_caller
        self.backup_caller = backup_caller

    def execute_with_fallback(self, query: str) -> Dict[str, Any]:
        try:
            res = self.primary_caller(query)
            return {"source": "primary", "result": res}
        except Exception as exc:
            try:
                res = self.backup_caller(query)
                return {"source": "backup", "result": res, "primary_error": str(exc)}
            except Exception as backup_exc:
                return {"source": "failed", "error": f"Both failed: {exc}; {backup_exc}"}


client = FallbackA2AClient(
    primary_caller=lambda q: (_ for _ in ()).throw(ConnectionResetError("Primary Agent Unreachable")),
    backup_caller=lambda q: f"Backup resolved: {q}",
)

res = client.execute_with_fallback("Calculate portfolio delta")
assert res["source"] == "backup"
assert "Backup resolved" in res["result"]
assert "Primary Agent Unreachable" in res["primary_error"]
```

## Likely follow-ups

- When should an orchestrator failover versus retry with exponential backoff?
- How do circuit breakers prevent overwhelming a failing primary agent?

---

[← Q0672](../../batch_07_mcp_a2a_skills_assistants/0672_shared_blackboard_architecture_for_a2a_collaboration/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0674 →](../../batch_07_mcp_a2a_skills_assistants/0674_tracing_multi_agent_a2a_message_chains_with_correlation_ids/README.md)

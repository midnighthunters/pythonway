# Q0946 · Blast radius containment: rate-limiting agent tool invocations

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Easy |

## Question

Write Python code implementing an in-flight tool call governor that limits the maximum number of tool invocations an agent can execute within a single user conversation turn.

## Answer

An agent trapped in an infinite reasoning loop or hallucinating tool requirements can invoke APIs hundreds of times in seconds, saturating backend systems and incurring massive API charges.

A **Tool Call Governor** caps total tool executions per turn (e.g., maximum 5 tool calls per user turn).

```python
class ToolExecutionGovernor:
    def __init__(self, max_tool_calls_per_turn: int = 5):
        self.max_calls = max_tool_calls_per_turn
        self.call_count = 0

    def can_execute(self) -> bool:
        return self.call_count < self.max_calls

    def record_execution(self, tool_name: str) -> None:
        if not self.can_execute():
            raise RuntimeError(f"Tool execution ceiling ({self.max_calls}) breached for current turn.")
        self.call_count += 1

    def reset_turn(self) -> None:
        self.call_count = 0


governor = ToolExecutionGovernor(max_tool_calls_per_turn=3)

for i in range(3):
    assert governor.can_execute() is True
    governor.record_execution(f"tool_{i}")

assert governor.can_execute() is False
try:
    governor.record_execution("tool_overflow")
    assert False, "Should have raised RuntimeError"
except RuntimeError:
    pass

governor.reset_turn()
assert governor.can_execute() is True
```

## Likely follow-ups

- What should the agent do when its tool quota is exhausted (e.g. gracefully apologize to the user)?
- How does recursion limit configuration in LangGraph (`recursion_limit=25`) provide this protection?

---

[← Q0945](../../batch_10_ai_security_responsible_ai/0945_sql_query_ast_validation_and_blocking_ddl_dml_in_text_to/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0947 →](../../batch_10_ai_security_responsible_ai/0947_dual_custody_and_4_eyes_principle_enforcement_for_financial/README.md)

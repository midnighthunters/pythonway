# Q0682 · Skill composition: combining multiple skills for compound tasks

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

Write Python code for a compound workflow that sequences two independent skills (e.g. Trade Break Investigation followed by Notification Dispatch).

## Answer

```python
from typing import Any, Dict


class SkillRegistry:
    def __init__(self):
        self._skills = {}

    def register(self, name: str, fn):
        self._skills[name] = fn

    def execute(self, name: str, data: Any) -> Any:
        return self._skills[name](data)


def run_compound_workflow(trade_id: str, registry: SkillRegistry) -> Dict[str, Any]:
    investigation = registry.execute("investigate_break", trade_id)
    notification = registry.execute("notify_operations", {
        "trade_id": trade_id,
        "discrepancy": investigation["discrepancy"],
    })
    return {"investigation": investigation, "notification": notification}


reg = SkillRegistry()
reg.register("investigate_break", lambda tid: {"trade_id": tid, "discrepancy": "$450.00", "reason": "Fee mismatch"})
reg.register("notify_operations", lambda p: f"Alert dispatched to Ops team for {p['trade_id']} discrepancy {p['discrepancy']}")

res = run_compound_workflow("TRD-77", reg)
assert res["investigation"]["reason"] == "Fee mismatch"
assert "Alert dispatched" in res["notification"]
```

## Likely follow-ups

- How does the orchestrator determine which skills can be piped together?
- What happens if the output schema of Skill A does not match the input schema of Skill B?

---

[← Q0681](../../batch_07_mcp_a2a_skills_assistants/0681_sandboxing_skill_execution_in_isolated_runtimes/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0683 →](../../batch_07_mcp_a2a_skills_assistants/0683_skill_versioning_deprecation_and_rollback_in_production/README.md)

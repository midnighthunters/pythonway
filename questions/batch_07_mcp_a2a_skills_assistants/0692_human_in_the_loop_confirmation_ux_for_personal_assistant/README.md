# Q0692 · Human-in-the-loop confirmation UX for personal assistant actions

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

Write Python code implementing an action approval gate for high-impact personal assistant operations (e.g. sending emails or executing bookings).

## Answer

```python
from typing import Any, Callable, Dict


class ActionApprovalGate:
    def __init__(self, risk_threshold: float = 10000.0):
        self.risk_threshold = risk_threshold

    def evaluate_action(self, action_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        amount = payload.get("amount", 0.0)
        if amount >= self.risk_threshold or action_name in {"execute_trade", "delete_file"}:
            return {
                "requires_approval": True,
                "prompt": f"Approval required: Execute {action_name} with amount ${amount:,.2f}?",
                "status": "pending_confirmation",
            }
        return {"requires_approval": False, "status": "approved"}


gate = ActionApprovalGate(risk_threshold=5000.0)
res_low = gate.evaluate_action("transfer_funds", {"amount": 500.0})
assert res_low["requires_approval"] is False

res_high = gate.evaluate_action("transfer_funds", {"amount": 25000.0})
assert res_high["requires_approval"] is True
assert "Approval required" in res_high["prompt"]
```

## Likely follow-ups

- How should the UI present confirmation prompts to prevent "rubber-stamping"?
- What audit records must be logged when a human approves an action?

---

[← Q0691](../../batch_07_mcp_a2a_skills_assistants/0691_proactive_vs_reactive_assistant_behavior_triggers_and/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0693 →](../../batch_07_mcp_a2a_skills_assistants/0693_handling_multi_turn_conversational_context_drift/README.md)

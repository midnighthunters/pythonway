# Q0430 · Risk-tiered autonomy

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Human-in-the-loop | Medium |

## Question

Implement a policy that decides per tool call whether to auto-execute, require approval, or forbid it, based on the tool's category, the amount, and the user's role.

## Answer

```python
from decimal import Decimal

POLICY = {
    "read": {"default": "auto"},
    "communication": {"default": "approve", "internal_only_auto": True},
    "payment": {"auto_limit": Decimal("0"), "approve_limit": Decimal("10000"), "roles": {"payments_ops"}},
    "admin": {"default": "forbid"},
}


def decide(category: str, role: str, amount: Decimal | None = None, external: bool = False) -> str:
    rule = POLICY.get(category, {"default": "forbid"})
    if category == "payment":
        if role not in rule["roles"] or amount is None:
            return "forbid"
        if amount <= rule["auto_limit"]:
            return "auto"
        return "approve" if amount <= rule["approve_limit"] else "forbid"
    if category == "communication" and not external and rule.get("internal_only_auto"):
        return "auto"
    return rule["default"]


assert decide("read", "analyst") == "auto"
assert decide("communication", "analyst", external=False) == "auto"
assert decide("communication", "analyst", external=True) == "approve"
assert decide("payment", "payments_ops", Decimal("2500")) == "approve"
assert decide("payment", "payments_ops", Decimal("25000")) == "forbid"
assert decide("payment", "analyst", Decimal("10")) == "forbid"
assert decide("admin", "payments_ops") == "forbid" and decide("unknown", "x") == "forbid"
```

Unknown categories fail closed. Keep the policy in configuration or a policy engine (OPA or Cedar style), reviewed by risk owners, versioned, and applied in code at the dispatcher, never in the prompt. Start new agents at low autonomy and raise limits as evaluation and incident history justify it.

## Likely follow-ups

- What evidence would justify raising an agent's auto-execute limit?

---

[← Q0429](../../batch_05_agentic_patterns_orchestration/0429_approve_edit_or_reject_a_tool_call/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0431 →](../../batch_05_agentic_patterns_orchestration/0431_designing_agent_state/README.md)

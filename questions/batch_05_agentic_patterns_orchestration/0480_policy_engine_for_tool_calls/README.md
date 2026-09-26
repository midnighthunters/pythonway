# Q0480 · Policy engine for tool calls

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent safety | Medium |

## Question

Implement a small policy engine for agent tool calls: ordered rules with conditions on the tool, the user's role and the arguments, first match wins, default deny, and the matched rule id returned for audit.

## Answer

```python
from decimal import Decimal
from typing import Callable

Rule = tuple[str, str, Callable[[dict], bool]]

RULES: list[Rule] = [
    ("R1-deny-external-email-for-contractors", "deny",
     lambda c: c["tool"] == "send_email" and c["role"] == "contractor" and not c["args"]["to"].endswith("@corp.example")),
    ("R2-approve-large-refunds", "approve",
     lambda c: c["tool"] == "issue_refund" and Decimal(c["args"]["amount"]) > Decimal("200")),
    ("R3-allow-refunds", "allow", lambda c: c["tool"] == "issue_refund" and c["role"] in {"support", "ops"}),
    ("R4-allow-reads", "allow", lambda c: c["tool"].startswith(("get_", "search_", "list_"))),
]


def evaluate(call: dict, rules: list[Rule] = RULES) -> tuple[str, str]:
    for rule_id, effect, cond in rules:
        try:
            if cond(call):
                return effect, rule_id
        except (KeyError, ValueError, ArithmeticError):
            return "deny", f"{rule_id}:malformed-arguments"
    return "deny", "default-deny"


assert evaluate({"tool": "get_balance", "role": "support", "args": {}}) == ("allow", "R4-allow-reads")
assert evaluate({"tool": "issue_refund", "role": "support", "args": {"amount": "50"}}) == ("allow", "R3-allow-refunds")
assert evaluate({"tool": "issue_refund", "role": "support", "args": {"amount": "900"}})[0] == "approve"
assert evaluate({"tool": "send_email", "role": "contractor", "args": {"to": "x@gmail.com"}})[0] == "deny"
assert evaluate({"tool": "delete_account", "role": "ops", "args": {}}) == ("deny", "default-deny")
assert evaluate({"tool": "issue_refund", "role": "ops", "args": {}})[0] == "deny"
```

Errors in a condition deny rather than allow. Rule ids in the audit log make every decision explainable. At platform scale, use a policy language and engine (OPA/Rego, Cedar) with policy tests, so risk and security teams can review the policies without reading application code.

## Likely follow-ups

- Why is rule order significant here, and how would you test it?

---

[← Q0479](../../batch_05_agentic_patterns_orchestration/0479_guardrails_on_agent_actions/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0481 →](../../batch_05_agentic_patterns_orchestration/0481_per_user_rate_limits_on_agent_tools/README.md)

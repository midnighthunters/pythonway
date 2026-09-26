# Q0474 · Route exceptions to remediation playbooks

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent tools | Medium |

## Question

Implement the playbook router for trade breaks: classify by comparing the trade and confirmation fields, apply tolerances, and return the playbook, whether it can auto-execute, and whether approval is required.

## Answer

```python
from datetime import date
from decimal import Decimal


def route_break(trade: dict, confirm: dict, px_tol: Decimal = Decimal("0.01"),
                auto_limit: Decimal = Decimal("1000")) -> dict:
    if trade["ssi"] != confirm["ssi"]:
        return {"playbook": "ssi_mismatch", "auto": False, "approval": "operations_and_fraud"}
    if trade["qty"] != confirm["qty"]:
        return {"playbook": "request_amended_confirm", "auto": True, "approval": None}
    px_diff = abs(Decimal(trade["px"]) - Decimal(confirm["px"]))
    if px_diff:
        impact = px_diff * trade["qty"]
        if px_diff <= px_tol and impact <= auto_limit:
            return {"playbook": "price_amend", "auto": False, "approval": "analyst", "impact": impact}
        return {"playbook": "price_dispute", "auto": False, "approval": "senior_analyst", "impact": impact}
    if trade["settle"] != confirm["settle"] and abs((trade["settle"] - confirm["settle"]).days) <= 1:
        return {"playbook": "timing_difference", "auto": True, "approval": None}
    return {"playbook": "investigate_manually", "auto": False, "approval": "analyst"}


base = {"qty": 1000, "px": "101.20", "ssi": "SSI-GB-1", "settle": date(2026, 10, 2)}
assert route_break(base, {**base, "px": "101.21"})["playbook"] == "price_amend"
assert route_break(base, {**base, "px": "102.50"})["approval"] == "senior_analyst"
assert route_break(base, {**base, "ssi": "SSI-XX-9"}) == {"playbook": "ssi_mismatch", "auto": False,
                                                           "approval": "operations_and_fraud"}
assert route_break(base, {**base, "settle": date(2026, 10, 3)})["playbook"] == "timing_difference"
assert route_break(base, {**base, "qty": 900})["auto"] is True
```

The rules are checked in order of risk: SSI changes first, because they are the classic payment-fraud vector. Playbooks in code give consistent, auditable decisions. The agent adds value by gathering evidence, handling unstructured confirmations (PDF or email parsing), and drafting counterparty messages.

## Likely follow-ups

- How would you add a new break type without redeploying the agent?

---

[← Q0473](../../batch_05_agentic_patterns_orchestration/0473_trade_break_remediation_agent/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0475 →](../../batch_05_agentic_patterns_orchestration/0475_agentic_code_fix_loop_design/README.md)

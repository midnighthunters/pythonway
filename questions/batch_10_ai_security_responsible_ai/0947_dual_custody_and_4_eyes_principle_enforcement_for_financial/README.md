# Q0947 · Dual-custody and 4-eyes principle enforcement for financial actions

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Explain the 4-eyes principle (dual custody) in banking operations, and write Python code ensuring high-value agent actions require cryptographic approval from two distinct authorized principals.

## Answer

In financial institutions, high-value transfers (e.g. > $1M) or credit limit modifications require **dual-control** (the 4-eyes principle): no single individual can initiate and approve the transaction alone. The initiator (Maker) and approver (Checker) must be distinct authorized employees.

```python
from typing import Dict, List, Set


class DualCustodyWorkflow:
    def __init__(self):
        # Maps tx_id -> {"maker": str, "checkers": set, "status": str}
        self.transactions: Dict[str, Dict] = {}

    def initiate_transaction(self, tx_id: str, maker_id: str, amount: float) -> None:
        self.transactions[tx_id] = {
            "maker": maker_id,
            "amount": amount,
            "checkers": set(),
            "status": "INITIATED",
        }

    def add_approval(self, tx_id: str, approver_id: str) -> str:
        tx = self.transactions.get(tx_id)
        if not tx:
            raise ValueError("Transaction not found")

        # Maker cannot approve their own transaction!
        if approver_id == tx["maker"]:
            raise PermissionError("Maker cannot act as Checker (Dual-custody violation).")

        tx["checkers"].add(approver_id)

        # 4-eyes principle: requires at least 1 distinct authorized checker
        if len(tx["checkers"]) >= 1:
            tx["status"] = "APPROVED"
        return tx["status"]


dc = DualCustodyWorkflow()
dc.initiate_transaction("tx_500", maker_id="trader_alice", amount=2_000_000.0)

# Alice attempts to approve her own transaction -> Rejected
try:
    dc.add_approval("tx_500", approver_id="trader_alice")
    assert False, "Should have raised PermissionError"
except PermissionError:
    pass

# Bob (risk manager) approves -> Approved
status = dc.add_approval("tx_500", approver_id="manager_bob")
assert status == "APPROVED"
```

## Likely follow-ups

- How does the 4-eyes principle prevent internal employee collusion and rogue trader fraud?
- How is dual custody audited under SOX (Sarbanes-Oxley) compliance?

---

[← Q0946](../../batch_10_ai_security_responsible_ai/0946_blast_radius_containment_rate_limiting_agent_tool/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0948 →](../../batch_10_ai_security_responsible_ai/0948_preventing_recursive_agent_loop_runaway_and_infinite_loop/README.md)

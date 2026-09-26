# Q0498 · Tamper-evident audit trail for agent actions

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Governance | Medium |

## Question

Implement a hash-chained audit log for agent actions, so any modification or deletion of past records is detectable during verification.

## Answer

```python
import hashlib
import json


def _hash(record: dict, prev: str) -> str:
    return hashlib.sha256((prev + json.dumps(record, sort_keys=True)).encode()).hexdigest()


class AuditLog:
    def __init__(self) -> None:
        self.entries: list[dict] = []

    def append(self, record: dict) -> str:
        prev = self.entries[-1]["hash"] if self.entries else "genesis"
        h = _hash(record, prev)
        self.entries.append({"record": record, "prev": prev, "hash": h})
        return h

    def verify(self) -> int | None:
        prev = "genesis"
        for i, e in enumerate(self.entries):
            if e["prev"] != prev or _hash(e["record"], prev) != e["hash"]:
                return i
            prev = e["hash"]
        return None


log = AuditLog()
log.append({"run": "r1", "tool": "get_invoice", "actor": "agent:refunds@1.4"})
log.append({"run": "r1", "tool": "issue_refund", "amount": "90.00", "approved_by": "tom"})
log.append({"run": "r1", "event": "completed"})
assert log.verify() is None
log.entries[1]["record"]["amount"] = "9000.00"
assert log.verify() == 1
del log.entries[1]
assert log.verify() == 1
```

Editing an amount or deleting an entry breaks the chain from that point on. Chaining detects tampering but doesn't prevent it. Anchor the latest hash externally (write it periodically to WORM storage or a separate system), and store the logs in append-only stores with restricted access. Record the agent version, the user and the approver on every action.

## Likely follow-ups

- Why must the head hash be anchored somewhere the log writer can't modify?

---

[← Q0497](../../batch_05_agentic_patterns_orchestration/0497_explain_what_the_agent_did/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0499 →](../../batch_05_agentic_patterns_orchestration/0499_design_an_agentic_orchestration_platform_for_llm_suite/README.md)

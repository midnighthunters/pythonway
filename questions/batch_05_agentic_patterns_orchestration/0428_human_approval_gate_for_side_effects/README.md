# Q0428 · Human approval gate for side effects

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Human-in-the-loop | Medium |

## Question

Implement an approval gate: read tools execute immediately, while write tools create a pending approval ticket. The run pauses until a human resolves the ticket, and then the call is executed or the rejection is returned to the model.

## Answer

```python
import itertools
from typing import Callable


class ApprovalGate:
    def __init__(self, tools: dict[str, tuple[str, Callable]]) -> None:
        self.tools = tools
        self.pending: dict[int, dict] = {}
        self._ids = itertools.count(1)

    def request(self, name: str, args: dict, user: str) -> dict:
        effect, fn = self.tools[name]
        if effect == "read":
            return {"status": "executed", "result": fn(**args)}
        ticket = next(self._ids)
        self.pending[ticket] = {"name": name, "args": args, "user": user}
        return {"status": "pending_approval", "ticket": ticket,
                "summary": f"{name}({', '.join(f'{k}={v}' for k, v in args.items())})"}

    def resolve(self, ticket: int, approver: str, approved: bool, reason: str = "") -> dict:
        req = self.pending.pop(ticket)
        if approver == req["user"] and req["name"] == "release_payment":
            raise PermissionError("four-eyes rule: requester cannot approve their own payment")
        if not approved:
            return {"status": "rejected", "reason": reason or "rejected by reviewer"}
        _, fn = self.tools[req["name"]]
        return {"status": "executed", "result": fn(**req["args"]), "approved_by": approver}


sent: list[str] = []
gate = ApprovalGate({"get_invoice": ("read", lambda invoice_id: {"id": invoice_id, "amount": "900.00"}),
                     "release_payment": ("write", lambda invoice_id: sent.append(invoice_id) or f"PAID {invoice_id}")})
assert gate.request("get_invoice", {"invoice_id": "INV-7"}, "priya")["status"] == "executed"
pending = gate.request("release_payment", {"invoice_id": "INV-7"}, "priya")
assert pending["status"] == "pending_approval" and sent == []
assert gate.resolve(pending["ticket"], "tom", approved=True)["result"] == "PAID INV-7"
t2 = gate.request("release_payment", {"invoice_id": "INV-8"}, "priya")["ticket"]
try:
    gate.resolve(t2, "priya", approved=True)
    raise AssertionError
except PermissionError:
    pass
```

Show the approver exactly what will run (the tool and its concrete arguments), not the model's description of it. Persist pending tickets (the agent may wait hours). Enforce segregation of duties (four-eyes) for financial actions. LangGraph implements the pause with `interrupt()` and a checkpointer, and resumes with `Command(resume=...)`.

## Likely follow-ups

- Why must the approver see the concrete arguments rather than the agent's summary?

---

[← Q0427](../../batch_05_agentic_patterns_orchestration/0427_deadline_propagation_across_nested_calls/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0429 →](../../batch_05_agentic_patterns_orchestration/0429_approve_edit_or_reject_a_tool_call/README.md)

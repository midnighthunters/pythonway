# Q0466 · Pause and resume an agent with generators

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Human-in-the-loop | Medium |

## Question

Model an agent as a generator that yields when it needs human input (approval) and resumes with the human's decision via `send()`. Write the driver that feeds decisions.

## Answer

```python
from typing import Generator


def refund_agent(invoice: str, amount: float) -> Generator[dict, dict, dict]:
    facts = {"invoice": invoice, "amount": amount}
    if amount > 100:
        decision = yield {"type": "approval_request", "action": "issue_refund", "args": facts}
        if not decision.get("approved"):
            return {"status": "rejected", "reason": decision.get("reason", "")}
    return {"status": "refunded", **facts}


def drive(gen: Generator, decide) -> dict:
    try:
        request = next(gen)
        while True:
            request = gen.send(decide(request))
    except StopIteration as done:
        return done.value


assert drive(refund_agent("INV-1", 50.0), decide=lambda r: {}) == {"status": "refunded", "invoice": "INV-1", "amount": 50.0}
assert drive(refund_agent("INV-2", 500.0), decide=lambda r: {"approved": True})["status"] == "refunded"
assert drive(refund_agent("INV-3", 500.0), decide=lambda r: {"approved": False, "reason": "duplicate"}) == {
    "status": "rejected", "reason": "duplicate"}
```

Generators make the pause point explicit, but they live in process memory, so a restart loses them. Durable frameworks persist the state at the pause (LangGraph's `interrupt()` saves a checkpoint, and `Command(resume=...)` continues possibly days later on another pod). The shape of the code is the same.

## Likely follow-ups

- What must be persisted so the pause survives a deployment?

---

[← Q0465](../../batch_05_agentic_patterns_orchestration/0465_stream_agent_progress_events/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0467 →](../../batch_05_agentic_patterns_orchestration/0467_observability_requirements_for_agents/README.md)

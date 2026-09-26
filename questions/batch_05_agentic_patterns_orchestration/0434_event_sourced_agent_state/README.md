# Q0434 · Event-sourced agent state

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | State management | Medium |

## Question

Model an agent run as an append-only event log, derive the current state by folding the events, and reconstruct the state at any earlier point for debugging.

## Answer

```python
from functools import reduce


def apply(state: dict, event: dict) -> dict:
    kind = event["type"]
    if kind == "task_started":
        return {"status": "running", "task": event["task"], "steps": [], "answer": None}
    if kind == "tool_called":
        return {**state, "steps": state["steps"] + [event["tool"]]}
    if kind == "approval_requested":
        return {**state, "status": "waiting_approval"}
    if kind == "approval_granted":
        return {**state, "status": "running"}
    if kind == "completed":
        return {**state, "status": "done", "answer": event["answer"]}
    raise ValueError(f"unknown event {kind}")


def state_at(events: list[dict], upto: int | None = None) -> dict:
    return reduce(apply, events[:upto], {})


log = [{"type": "task_started", "task": "refund INV-7"}, {"type": "tool_called", "tool": "get_invoice"},
       {"type": "approval_requested"}, {"type": "approval_granted"},
       {"type": "tool_called", "tool": "issue_refund"}, {"type": "completed", "answer": "Refunded 90.00"}]
assert state_at(log)["status"] == "done" and state_at(log)["steps"] == ["get_invoice", "issue_refund"]
assert state_at(log, 3)["status"] == "waiting_approval"
```

Benefits: a complete audit trail (who, what, when), time-travel debugging, and rebuilding projections (dashboards, analytics) from the same log. Costs: schema evolution for events (upcasters), snapshots for long logs, and storage. It fits regulated environments well, because nothing is overwritten.

## Likely follow-ups

- How would you handle an event type renamed in a later version?

---

[← Q0433](../../batch_05_agentic_patterns_orchestration/0433_durable_execution_for_long_running_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0435 →](../../batch_05_agentic_patterns_orchestration/0435_short_term_versus_long_term_agent_memory/README.md)

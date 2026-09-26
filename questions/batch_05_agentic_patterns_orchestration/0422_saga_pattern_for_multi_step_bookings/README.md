# Q0422 · Saga pattern for multi-step bookings

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Transactions | Hard |

## Question

A travel agent books flight, hotel and car in sequence across independent systems. Implement a saga: each step has an action and a compensation, and when a step fails, the completed steps are compensated in reverse order.

## Answer

```python
from typing import Callable


def run_saga(steps: list[tuple[str, Callable[[], str], Callable[[str], None]]]) -> dict:
    completed: list[tuple[str, str, Callable[[str], None]]] = []
    log = []
    for name, action, compensate in steps:
        try:
            ref = action()
            completed.append((name, ref, compensate))
            log.append(f"done:{name}:{ref}")
        except Exception as e:
            log.append(f"failed:{name}:{e}")
            for cname, cref, comp in reversed(completed):
                try:
                    comp(cref)
                    log.append(f"compensated:{cname}:{cref}")
                except Exception as ce:
                    log.append(f"compensation_failed:{cname}:{ce}")
            return {"status": "rolled_back", "log": log}
    return {"status": "committed", "log": log}


def car_fail():
    raise RuntimeError("no cars available")


cancelled: list[str] = []
steps = [("flight", lambda: "FL-123", cancelled.append), ("hotel", lambda: "HT-9", cancelled.append),
         ("car", car_fail, cancelled.append)]
out = run_saga(steps)
assert out["status"] == "rolled_back" and cancelled == ["HT-9", "FL-123"]
assert out["log"][-2:] == ["compensated:hotel:HT-9", "compensated:flight:FL-123"]
assert run_saga(steps[:2])["status"] == "committed"
```

Distributed systems rarely offer cross-system transactions, so sagas give eventual consistency through compensation. Production details:
- Persist the saga log after each step (so a crash can resume or compensate).
- Make actions and compensations idempotent (retries happen).
- Compensation can fail (a non-refundable fare), so escalate those to humans.
- Order the steps so the hardest-to-undo action goes last.

This is the pattern behind multi-agent rebooking with rollback.

## Likely follow-ups

- Why should the least reversible step go last?

---

[← Q0421](../../batch_05_agentic_patterns_orchestration/0421_critical_path_of_an_agent_workflow/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0423 →](../../batch_05_agentic_patterns_orchestration/0423_idempotency_keys_for_tool_calls/README.md)

# Q0410 · Re-planning after a failed step

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Planning patterns | Medium |

## Question

Extend plan-and-execute so that when a step fails, a re-planner receives the completed steps and the error and returns a revised remaining plan, with a cap on re-plans.

## Answer

```python
from typing import Callable


def execute_with_replanning(task: str, plan: list[dict], tools: dict[str, Callable],
                            replanner: Callable[[str, list, str], list[dict]], max_replans: int = 2) -> dict:
    done: list[tuple[dict, object]] = []
    replans = 0
    queue = list(plan)
    while queue:
        step = queue.pop(0)
        try:
            done.append((step, tools[step["tool"]](**step["args"])))
        except Exception as e:
            if replans == max_replans:
                return {"status": "failed", "done": done, "error": str(e), "replans": replans}
            replans += 1
            queue = replanner(task, done, f"{step['tool']} failed: {e}")
    return {"status": "ok", "done": done, "replans": replans}


def book_hotel(hotel: str) -> str:
    if hotel == "Grand":
        raise RuntimeError("sold out")
    return f"booked {hotel}"


tools = {"book_hotel": book_hotel, "notify": lambda msg: f"sent: {msg}"}
plan = [{"tool": "book_hotel", "args": {"hotel": "Grand"}}, {"tool": "notify", "args": {"msg": "Grand booked"}}]
replanner = lambda task, done, err: [{"tool": "book_hotel", "args": {"hotel": "Plaza"}},
                                     {"tool": "notify", "args": {"msg": "Plaza booked (Grand sold out)"}}]
out = execute_with_replanning("book a hotel", plan, tools, replanner)
assert out["status"] == "ok" and out["replans"] == 1
assert [r for _, r in out["done"]] == ["booked Plaza", "sent: Plaza booked (Grand sold out)"]
```

Note that the stale step ("notify: Grand booked") was replaced, not executed, which is why the re-planner gets the whole remaining plan rather than a single substitute step. Cap re-plans, and escalate to a human when the cap is hit.

## Likely follow-ups

- What context must the re-planner see to avoid repeating the failed choice?

---

[← Q0409](../../batch_05_agentic_patterns_orchestration/0409_plan_and_execute_agent/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0411 →](../../batch_05_agentic_patterns_orchestration/0411_reflection_and_self_correction_for_agents/README.md)

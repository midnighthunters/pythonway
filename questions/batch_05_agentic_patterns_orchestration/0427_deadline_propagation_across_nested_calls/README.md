# Q0427 · Deadline propagation across nested calls

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Concurrency | Medium |

## Question

A request has a 10-second deadline, and nested steps (LLM calls, tools, sub-agents) must never wait beyond it. Implement deadline propagation with `contextvars`, so inner code can ask how much time remains and nested scopes can only shorten the deadline.

## Answer

```python
import contextvars
from contextlib import contextmanager

_deadline = contextvars.ContextVar("deadline", default=float("inf"))


class DeadlineExceeded(Exception):
    pass


@contextmanager
def deadline(seconds: float, clock):
    new = min(_deadline.get(), clock() + seconds)
    token = _deadline.set(new)
    try:
        yield
    finally:
        _deadline.reset(token)


def remaining(clock) -> float:
    left = _deadline.get() - clock()
    if left <= 0:
        raise DeadlineExceeded("request deadline exceeded")
    return left


now = [100.0]
clock = lambda: now[0]
with deadline(10, clock):
    assert remaining(clock) == 10
    with deadline(30, clock):
        assert remaining(clock) == 10
    with deadline(3, clock):
        now[0] += 1
        assert remaining(clock) == 2
    now[0] += 9.5
    try:
        remaining(clock)
        raise AssertionError
    except DeadlineExceeded:
        pass
assert _deadline.get() == float("inf")
```

The inner 30-second scope can't extend the outer 10-second deadline. Use `remaining()` to set per-call timeouts (`wait_for(llm(...), timeout=remaining())`) and to skip optional steps when time is short. Across services, propagate the deadline in a header (as gRPC does), so remote agents respect it too.

## Likely follow-ups

- Which steps would you skip first when little time remains?

---

[← Q0426](../../batch_05_agentic_patterns_orchestration/0426_timeouts_and_cancellation_in_agent_runs/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0428 →](../../batch_05_agentic_patterns_orchestration/0428_human_approval_gate_for_side_effects/README.md)

# Q0426 · Timeouts and cancellation in agent runs

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Concurrency | Medium |

## Question

Enforce a wall-clock timeout on an async agent run, and make sure cleanup (releasing locks, recording partial state) happens when the run is cancelled.

## Answer

```python
import asyncio

events: list[str] = []


async def agent_run(steps: int) -> str:
    events.append("lock_acquired")
    try:
        for i in range(steps):
            await asyncio.sleep(0.02)
            events.append(f"step{i}")
        return "done"
    except asyncio.CancelledError:
        events.append("cancelled:partial_state_saved")
        raise
    finally:
        events.append("lock_released")


async def run_with_timeout(steps: int, timeout: float) -> str:
    try:
        return await asyncio.wait_for(agent_run(steps), timeout)
    except asyncio.TimeoutError:
        return "timed_out"


assert asyncio.run(run_with_timeout(2, 1.0)) == "done" and events[-1] == "lock_released"
events.clear()
assert asyncio.run(run_with_timeout(50, 0.05)) == "timed_out"
assert "cancelled:partial_state_saved" in events and events[-1] == "lock_released"
```

Cancellation arrives as `CancelledError` at an `await` point. Handle it to save state, then re-raise it, because swallowing it breaks cancellation semantics. Also cancel upstream LLM streams and HTTP requests when the user disconnects or a deadline passes, or you keep paying for tokens nobody reads.

## Likely follow-ups

- Why must you re-raise `CancelledError` after cleanup?

---

[← Q0425](../../batch_05_agentic_patterns_orchestration/0425_circuit_breaker_for_flaky_tools/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0427 →](../../batch_05_agentic_patterns_orchestration/0427_deadline_propagation_across_nested_calls/README.md)

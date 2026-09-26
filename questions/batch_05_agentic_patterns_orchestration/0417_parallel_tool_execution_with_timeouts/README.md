# Q0417 · Parallel tool execution with timeouts

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Concurrency | Medium |

## Question

A model requests three independent tool calls in one turn. Execute them concurrently with per-call timeouts, and return partial results (with errors) in the original order.

## Answer

```python
import asyncio
import time
from typing import Awaitable, Callable


async def run_parallel(calls: list[tuple[str, Callable[[], Awaitable]]], timeout: float) -> list[dict]:
    async def one(call_id: str, fn: Callable[[], Awaitable]) -> dict:
        try:
            return {"id": call_id, "ok": True, "result": await asyncio.wait_for(fn(), timeout)}
        except asyncio.TimeoutError:
            return {"id": call_id, "ok": False, "error": "timeout"}
        except Exception as e:
            return {"id": call_id, "ok": False, "error": f"{type(e).__name__}: {e}"}

    return await asyncio.gather(*(one(cid, fn) for cid, fn in calls))


async def delayed(value, delay):
    await asyncio.sleep(delay)
    return value


async def failing():
    raise ValueError("bad account")


start = time.perf_counter()
res = asyncio.run(run_parallel([("c1", lambda: delayed("fx=1.27", 0.05)), ("c2", lambda: delayed("slow", 1.0)),
                                ("c3", failing), ("c4", lambda: delayed("bal=100", 0.05))], timeout=0.2))
elapsed = time.perf_counter() - start
assert [r["id"] for r in res] == ["c1", "c2", "c3", "c4"]
assert res[1]["error"] == "timeout" and "ValueError" in res[2]["error"] and res[3]["result"] == "bal=100"
assert elapsed < 0.6
```

Total latency is roughly the slowest call (capped by the timeout), not the sum. Only parallelise calls that are independent and safe to run concurrently: read calls usually are, and two writes to the same account usually aren't. Every result, including errors, goes back to the model with its `tool_call_id`.

## Likely follow-ups

- How would you cap concurrency per downstream API?

---

[← Q0416](../../batch_05_agentic_patterns_orchestration/0416_handoff_loop_with_ping_pong_protection/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0418 →](../../batch_05_agentic_patterns_orchestration/0418_fan_out_and_fan_in_with_bounded_concurrency/README.md)

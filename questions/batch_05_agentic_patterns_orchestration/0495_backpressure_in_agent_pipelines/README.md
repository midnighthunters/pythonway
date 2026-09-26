# Q0495 · Backpressure in agent pipelines

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Concurrency | Medium |

## Question

A producer enqueues documents faster than agent workers can process them. Implement backpressure with a bounded asyncio queue, so the producer slows down instead of exhausting memory, and verify the queue never exceeds its bound.

## Answer

```python
import asyncio


async def pipeline(n_items: int, maxsize: int, workers: int) -> dict:
    q: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
    peak = 0
    done: list[int] = []

    async def producer():
        nonlocal peak
        for i in range(n_items):
            await q.put(i)
            peak = max(peak, q.qsize())
        for _ in range(workers):
            await q.put(None)

    async def worker():
        while (item := await q.get()) is not None:
            await asyncio.sleep(0.002)
            done.append(item)

    await asyncio.gather(producer(), *(worker() for _ in range(workers)))
    return {"processed": len(done), "peak_queue": peak}


out = asyncio.run(pipeline(n_items=100, maxsize=5, workers=3))
assert out["processed"] == 100 and out["peak_queue"] <= 5
```

`await q.put()` blocks when the queue is full, which pushes back on the producer automatically. Across services, backpressure comes from bounded broker queues, consumer lag monitoring, rate limits (429 with `Retry-After`) and autoscaling workers on queue depth. Without it, a burst (a morning of disruptions) turns into memory exhaustion or a provider quota wall.

## Likely follow-ups

- What should the API tier do when the internal queue is full?

---

[← Q0494](../../batch_05_agentic_patterns_orchestration/0494_fair_scheduling_of_agent_jobs_across_tenants/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0496 →](../../batch_05_agentic_patterns_orchestration/0496_cross_user_isolation_in_shared_agents/README.md)

# Q0418 · Fan-out and fan-in with bounded concurrency

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Concurrency | Medium |

## Question

Implement map-reduce over sub-tasks with an async worker per item, bounded concurrency, and a reduce step, for example analysing 20 contracts in parallel and combining the findings.

## Answer

```python
import asyncio
from typing import Awaitable, Callable


async def fan_out_fan_in(items: list, worker: Callable[[object], Awaitable[dict]], reduce: Callable[[list[dict]], dict],
                         concurrency: int = 4) -> dict:
    sem = asyncio.Semaphore(concurrency)
    peak = active = 0

    async def run(item):
        nonlocal peak, active
        async with sem:
            active += 1
            peak = max(peak, active)
            try:
                return await worker(item)
            finally:
                active -= 1

    results = await asyncio.gather(*(run(i) for i in items), return_exceptions=True)
    ok = [r for r in results if not isinstance(r, BaseException)]
    failed = [items[i] for i, r in enumerate(results) if isinstance(r, BaseException)]
    return {**reduce(ok), "failed": failed, "peak_concurrency": peak}


async def analyse(contract_id: int) -> dict:
    await asyncio.sleep(0.01)
    if contract_id == 13:
        raise RuntimeError("unreadable PDF")
    return {"id": contract_id, "has_change_of_control": contract_id % 5 == 0}


summary = asyncio.run(fan_out_fan_in(list(range(1, 21)), analyse,
                                     lambda rs: {"flagged": sorted(r["id"] for r in rs if r["has_change_of_control"])}))
assert summary["flagged"] == [5, 10, 15, 20] and summary["failed"] == [13] and summary["peak_concurrency"] <= 4
```

`return_exceptions=True` keeps one bad document from sinking the batch. Report failures explicitly, so the combined answer never silently omits a contract. In LangGraph, the same pattern uses `Send` to fan out to parallel node instances.

## Likely follow-ups

- How would you make the final answer state which documents it couldn't analyse?

---

[← Q0417](../../batch_05_agentic_patterns_orchestration/0417_parallel_tool_execution_with_timeouts/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0419 →](../../batch_05_agentic_patterns_orchestration/0419_topological_sort_of_a_task_graph/README.md)

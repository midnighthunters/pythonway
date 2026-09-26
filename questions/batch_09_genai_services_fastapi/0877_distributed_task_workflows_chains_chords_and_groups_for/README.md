# Q0877 · Distributed task workflows: Chains, Chords, and Groups for parallel map-reduce

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Hard |

## Question

Explain distributed task orchestration patterns in Celery (Canvas): Chain, Group, and Chord, and write Python code simulating a Chord (parallel map + reduce callback).

## Answer

In GenAI workflows:
1. **Chain (Sequential)**: Output of task A feeds task B (e.g. Extract text -> Summarize).
2. **Group (Parallel Map)**: Tasks A1, A2, A3 execute simultaneously across different workers.
3. **Chord (Parallel Map + Reduce)**: Executes a Group of tasks in parallel, and triggers a Callback task only when all tasks in the group finish.

```python
import asyncio
from typing import Callable, List


async def map_task(chunk_text: str) -> str:
    await asyncio.sleep(0.01)
    return f"Summary({chunk_text})"


async def reduce_task(summaries: List[str]) -> str:
    await asyncio.sleep(0.005)
    return " | ".join(summaries)


async def execute_chord(
    items: List[str],
    map_fn: Callable,
    reduce_fn: Callable,
) -> str:
    # Parallel Map
    tasks = [map_fn(item) for item in items]
    map_results = await asyncio.gather(*tasks)

    # Reduce callback
    final_output = await reduce_fn(map_results)
    return final_output


async def main():
    chunks = ["Section 1: Balance Sheet", "Section 2: Income Statement", "Section 3: Cash Flow"]
    res = await execute_chord(chunks, map_task, reduce_task)

    assert "Summary(Section 1: Balance Sheet)" in res
    assert "Summary(Section 3: Cash Flow)" in res
    assert " | " in res


asyncio.run(main())
```

## Likely follow-ups

- What happens if one task in the Group fails inside a Celery Chord?
- How does Celery store intermediate Chord results in Redis before the callback executes?

---

[← Q0876](../../batch_09_genai_services_fastapi/0876_cancelling_in_flight_async_queue_jobs_on_user_request/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0878 →](../../batch_09_genai_services_fastapi/0878_worker_memory_leak_mitigation_recycling_worker_processes/README.md)

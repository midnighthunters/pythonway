# Q0849 · Priority queues for Tier-1 bank workloads versus batch background jobs

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Hard |

## Question

Write Python code implementing an asynchronous priority queue for LLM requests, ensuring high-priority interactive trading desk requests preempt low-priority document batch indexing.

## Answer

In financial institutions, an interactive algorithmic trading assistant must take precedence over an overnight batch job summarizing 5,000 regulatory filings. An `asyncio.PriorityQueue` ensures higher-priority requests execute first.

```python
import asyncio
from typing import Any, Tuple


class PrioritizedLLMExecutor:
    def __init__(self):
        # Stores tuples: (priority_int, task_id, prompt)
        # Lower integer = higher priority (0 is urgent, 10 is low)
        self.queue: asyncio.PriorityQueue[Tuple[int, int, str]] = asyncio.PriorityQueue()

    async def submit(self, priority: int, task_id: int, prompt: str) -> None:
        await self.queue.put((priority, task_id, prompt))

    async def process_next(self) -> Tuple[int, int, str]:
        return await self.queue.get()


async def main():
    executor = PrioritizedLLMExecutor()

    # Submit batch background jobs (Priority 5)
    await executor.submit(priority=5, task_id=101, prompt="Batch PDF 1")
    await executor.submit(priority=5, task_id=102, prompt="Batch PDF 2")

    # Submit urgent real-time trader query (Priority 0)
    await executor.submit(priority=0, task_id=999, prompt="Trader Urgent Quote")

    # First item processed must be priority 0
    p1, tid1, prompt1 = await executor.process_next()
    assert tid1 == 999
    assert p1 == 0

    # Next items are priority 5
    p2, tid2, _ = await executor.process_next()
    assert tid2 == 101


asyncio.run(main())
```

## Likely follow-ups

- How do you prevent starvation of low-priority background tasks under continuous high-priority load?
- How is priority scheduling implemented across distributed Celery or RabbitMQ queues?

---

[← Q0848](../../batch_09_genai_services_fastapi/0848_concurrency_limiting_with_asyncio_semaphore_to_prevent/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0850 →](../../batch_09_genai_services_fastapi/0850_circuit_breaker_pattern_for_downstream_llm_provider_outages/README.md)

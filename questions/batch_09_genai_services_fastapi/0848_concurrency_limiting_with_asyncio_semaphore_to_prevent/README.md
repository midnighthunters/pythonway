# Q0848 · Concurrency limiting with asyncio Semaphore to prevent gateway saturation

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Medium |

## Question

Write Python code using `asyncio.Semaphore` to cap concurrent downstream LLM requests, queuing excess calls and preventing connection pool starvation.

## Answer

Uncontrolled concurrency in async FastAPI services can overwhelm downstream Azure OpenAI or AWS Bedrock quotas, triggering cascade failures. An `asyncio.Semaphore` restricts concurrent outbound requests to a fixed ceiling.

```python
import asyncio
from typing import List


class ConcurrencyThrottler:
    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.current_active = 0
        self.peak_active = 0

    async def run_with_throttle(self, task_id: int) -> str:
        async with self.semaphore:
            self.current_active += 1
            if self.current_active > self.peak_active:
                self.peak_active = self.current_active

            # Simulate outbound LLM API call
            await asyncio.sleep(0.01)
            self.current_active -= 1
            return f"Task {task_id} done"


async def main():
    throttler = ConcurrencyThrottler(max_concurrent=3)
    # Launch 10 tasks concurrently
    tasks = [throttler.run_with_throttle(i) for i in range(10)]
    results = await asyncio.gather(*tasks)

    assert len(results) == 10
    # Peak active requests must never exceed semaphore limit of 3
    assert throttler.peak_active <= 3


asyncio.run(main())
```

## Likely follow-ups

- What happens if a caller times out while waiting to acquire the semaphore?
- How do you configure HTTP client connection pool limits (`limits=httpx.Limits(max_connections=100)`)?

---

[← Q0847](../../batch_09_genai_services_fastapi/0847_http_429_retry_after_headers_and_client_cooperative_backoff/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0849 →](../../batch_09_genai_services_fastapi/0849_priority_queues_for_tier_1_bank_workloads_versus_batch/README.md)

# Q0876 · Cancelling in-flight async queue jobs on user request

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code demonstrating how an in-flight background worker cooperatively checks for a cancellation signal in Redis and cleanly aborts execution.

## Answer

If a user clicks "Cancel" on a long-running research report, continuing to invoke paid LLM APIs wastes money and compute. Workers must periodically check a cancellation flag between execution steps.

```python
import asyncio
from typing import Dict


class MockRedisCancellationRegistry:
    def __init__(self):
        self.flags: Dict[str, bool] = {}

    def set_cancel(self, job_id: str) -> None:
        self.flags[job_id] = True

    def is_cancelled(self, job_id: str) -> bool:
        return self.flags.get(job_id, False)


async def execute_multi_step_agent_job(
    job_id: str, registry: MockRedisCancellationRegistry
) -> dict:
    steps_completed = 0
    for step in range(1, 10):
        # Cooperative cancellation check before each step
        if registry.is_cancelled(job_id):
            return {"status": "ABORTED", "steps_completed": steps_completed}

        await asyncio.sleep(0.01)  # Simulate LLM tool step
        steps_completed += 1

    return {"status": "COMPLETED", "steps_completed": steps_completed}


async def main():
    reg = MockRedisCancellationRegistry()
    job_id = "job_cancel_01"

    # Start job task
    task = asyncio.create_task(execute_multi_step_agent_job(job_id, reg))

    # Cancel after 25ms (during step 3)
    await asyncio.sleep(0.025)
    reg.set_cancel(job_id)

    result = await task
    assert result["status"] == "ABORTED"
    assert result["steps_completed"] < 10


asyncio.run(main())
```

## Likely follow-ups

- Why cannot you simply run `kill -9` on a Celery worker to abort a task?
- How does `asyncio.Task.cancel()` propagate cancellation compared to cooperative polling?

---

[← Q0875](../../batch_09_genai_services_fastapi/0875_real_time_progress_updates_via_redis_pubsub_during_batch/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0877 →](../../batch_09_genai_services_fastapi/0877_distributed_task_workflows_chains_chords_and_groups_for/README.md)

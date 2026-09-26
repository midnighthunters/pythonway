# Q0871 · ARQ async Redis job queue implementation for long-running document indexing

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Hard |

## Question

Write Python code demonstrating an asynchronous background job queue runner (simulating ARQ or Redis Streams) that enqueues document indexing tasks and checks job execution status.

## Answer

Parsing a 500-page prospectus, generating 2,000 embeddings, and indexing them in a vector database takes 2-5 minutes. ARQ is a high-performance asyncio-native job queue for Python backed by Redis, avoiding synchronous blocking.

```python
import asyncio
import uuid
from typing import Any, Dict, Optional


class MockArqJobQueue:
    def __init__(self):
        # Structure: job_id -> {"status": str, "result": Any}
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.queue: asyncio.Queue[str] = asyncio.Queue()

    async def enqueue(self, task_func: str, *args, **kwargs) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {"status": "QUEUED", "result": None}
        await self.queue.put(job_id)
        # Launch worker processing
        asyncio.create_task(self._worker_execute(job_id, task_func, args))
        return job_id

    async def _worker_execute(self, job_id: str, task_func: str, args: tuple) -> None:
        self.jobs[job_id]["status"] = "RUNNING"
        await asyncio.sleep(0.02)  # Simulate async indexing work
        self.jobs[job_id]["status"] = "COMPLETED"
        self.jobs[job_id]["result"] = f"Processed {args[0]} chunks"

    async def get_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)


async def main():
    queue = MockArqJobQueue()
    job_id = await queue.enqueue("index_document", 250)

    status_initial = await queue.get_status(job_id)
    assert status_initial["status"] in ["QUEUED", "RUNNING"]

    await asyncio.sleep(0.05)  # Wait for worker completion

    status_final = await queue.get_status(job_id)
    assert status_final["status"] == "COMPLETED"
    assert status_final["result"] == "Processed 250 chunks"


asyncio.run(main())
```

## Likely follow-ups

- Why is ARQ more lightweight than Celery for purely asynchronous Python workloads?
- How do you handle job deduplication in ARQ using job ID hashes?

---

[← Q0870](../../batch_09_genai_services_fastapi/0870_cors_csrf_and_security_headers_middleware_for_genai/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0872 →](../../batch_09_genai_services_fastapi/0872_celery_worker_configuration_for_cpu_bound_text_splitting/README.md)

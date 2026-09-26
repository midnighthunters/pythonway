# Q0885 · Testing async workers in isolation with mocks and test runners

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Easy |

## Question

Write Python code demonstrating how to unit-test an asynchronous queue consumer function in isolation using dependency injection and mock clients.

## Answer

Unit testing queue workers without spinning up real RabbitMQ, Redis, or cloud LLM infrastructure ensures fast and deterministic CI pipelines. Passing mock adapters allows validating business logic and error handling.

```python
import asyncio
from typing import Dict


class MockSummarizerClient:
    async def summarize(self, text: str) -> str:
        return f"Summary: {text[:20]}..."


async def process_queue_message(payload: dict, client: MockSummarizerClient) -> dict:
    if "text" not in payload:
        raise ValueError("Missing 'text' field in payload")
    summary = await client.summarize(payload["text"])
    return {
        "job_id": payload["job_id"],
        "status": "SUCCESS",
        "result": summary,
    }


async def test_worker_logic():
    client = MockSummarizerClient()
    payload = {"job_id": "test_42", "text": "JPMorgan Chase earnings report for Q3"}
    res = await process_queue_message(payload, client)

    assert res["status"] == "SUCCESS"
    assert res["job_id"] == "test_42"
    assert "JPMorgan Chase" in res["result"]


asyncio.run(test_worker_logic())
```

## Likely follow-ups

- How do you test retry behavior when the mock client raises a temporary network error?
- How does `celery.contrib.testing` provide in-memory task execution for Pytest?

---

[← Q0884](../../batch_09_genai_services_fastapi/0884_throttling_worker_consumption_to_match_downstream_cloud_api/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0886 →](../../batch_09_genai_services_fastapi/0886_multi_stage_dockerfile_for_fastapi_genai_microservices_with/README.md)

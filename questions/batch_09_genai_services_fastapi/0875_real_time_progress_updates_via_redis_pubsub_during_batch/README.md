# Q0875 · Real-time progress updates via Redis PubSub during batch jobs

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code implementing a Redis Pub/Sub progress broadcaster where background queue workers publish percent-complete updates and a subscriber stream receives them.

## Answer

Long-running jobs (such as fine-tuning data prep or batch document summarization) require real-time progress feedback (e.g. "Processing chunk 45/100 (45%)"). Redis Pub/Sub decouples background workers from frontend WebSocket connection managers.

```python
import asyncio
from typing import Dict, List


class MockRedisPubSubBus:
    def __init__(self):
        self.subscribers: Dict[str, List[asyncio.Queue]] = {}

    def subscribe(self, channel: str) -> asyncio.Queue:
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        q = asyncio.Queue()
        self.subscribers[channel].append(q)
        return q

    async def publish(self, channel: str, message: dict) -> None:
        subs = self.subscribers.get(channel, [])
        for q in subs:
            await q.put(message)


async def worker_task(bus: MockRedisPubSubBus, job_id: str, total_steps: int):
    for step in range(1, total_steps + 1):
        await asyncio.sleep(0.005)
        pct = int((step / total_steps) * 100)
        await bus.publish(f"job_progress:{job_id}", {"step": step, "percent": pct})


async def main():
    bus = MockRedisPubSubBus()
    job_id = "job_99"
    progress_stream = bus.subscribe(f"job_progress:{job_id}")

    # Launch worker
    asyncio.create_task(worker_task(bus, job_id, total_steps=4))

    # Read events from subscriber
    received = []
    for _ in range(4):
        msg = await progress_stream.get()
        received.append(msg["percent"])

    assert received == [25, 50, 75, 100]


asyncio.run(main())
```

## Likely follow-ups

- What happens if a subscriber disconnects while messages are being published in Redis Pub/Sub (at-most-once delivery)?
- When should you use Redis Streams instead of Redis Pub/Sub for guaranteed progress delivery?

---

[← Q0874](../../batch_09_genai_services_fastapi/0874_job_status_tracking_state_machine_pending_running_success/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0876 →](../../batch_09_genai_services_fastapi/0876_cancelling_in_flight_async_queue_jobs_on_user_request/README.md)

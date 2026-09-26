# Q0854 · Streaming backpressure handling when slow clients cannot consume tokens

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI streaming | Hard |

## Question

Explain how TCP and async generator backpressure manifests in Server-Sent Events (SSE) streaming, and write Python code simulating token queue buffering with drop/timeout on slow consumers.

## Answer

When an LLM produces 80 tokens/sec but a client is on a 2G mobile link or an overloaded UI thread consuming only 10 tokens/sec:
1. Tokens buffer in the server's application memory (OS TCP send buffer fills, then Uvicorn buffer fills).
2. Without backpressure controls, memory consumption skyrockets on high-concurrency servers.
3. Mitigation: Use bounded `asyncio.Queue`. When the queue fills to max capacity, either pause the upstream producer or disconnect the slow client.

```python
import asyncio
from typing import AsyncGenerator


class BackpressureTokenBuffer:
    def __init__(self, max_buffer_size: int = 5):
        self.queue: asyncio.Queue[str] = asyncio.Queue(maxsize=max_buffer_size)
        self.dropped_tokens = 0

    async def produce_token(self, token: str) -> bool:
        try:
            # Non-blocking put with immediate timeout to detect slow consumer
            self.queue.put_nowait(token)
            return True
        except asyncio.QueueFull:
            self.dropped_tokens += 1
            return False

    async def consume_token(self) -> str:
        return await self.queue.get()


async def main():
    buffer = BackpressureTokenBuffer(max_buffer_size=3)

    # Fast producer pushes 5 tokens
    p1 = await buffer.produce_token("token_1")
    p2 = await buffer.produce_token("token_2")
    p3 = await buffer.produce_token("token_3")
    p4 = await buffer.produce_token("token_4")  # Exceeds buffer

    assert p1 and p2 and p3 is True
    assert p4 is False
    assert buffer.dropped_tokens == 1

    # Consumer drains
    c1 = await buffer.consume_token()
    assert c1 == "token_1"


asyncio.run(main())
```

## Likely follow-ups

- How does `uvicorn` and `httptools` handle slow consumer TCP window zero notifications?
- Why is client disconnect detection critical when dropping tokens?

---

[← Q0853](../../batch_09_genai_services_fastapi/0853_request_deduplication_middleware_for_idempotent_chat/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0855 →](../../batch_09_genai_services_fastapi/0855_measuring_time_to_first_token_and_inter_token_latency_in/README.md)

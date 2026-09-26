# Q0865 · Asynchronous generator cancellation and memory cleanup on disconnect

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI streaming | Hard |

## Question

Write Python code demonstrating proper resource cleanup (closing DB cursors, releasing GPU locks) when an async generator is abruptly cancelled by a client disconnect.

## Answer

When a user closes their browser or navigates away during a 30-second token generation, the server's async generator must detect cancellation and execute `finally` blocks to prevent resource leaks (dangling database transactions, unclosed network sockets).

```python
import asyncio
from typing import AsyncGenerator


class ResourceTracker:
    def __init__(self):
        self.lock_acquired = False
        self.cleanup_done = False


tracker = ResourceTracker()


async def resource_intensive_generator() -> AsyncGenerator[str, None]:
    tracker.lock_acquired = True
    try:
        yield "Chunk 1"
        await asyncio.sleep(0.01)
        yield "Chunk 2"
        await asyncio.sleep(1.0)  # Client disconnects during this sleep
        yield "Chunk 3"
    finally:
        # Guaranteed cleanup upon GeneratorExit or asyncio.CancelledError
        tracker.lock_acquired = False
        tracker.cleanup_done = True


async def main():
    gen = resource_intensive_generator()
    chunk1 = await gen.asend(None)
    assert chunk1 == "Chunk 1"
    assert tracker.lock_acquired is True

    # Simulate client abrupt disconnect by closing generator
    await gen.aclose()
    assert tracker.lock_acquired is False
    assert tracker.cleanup_done is True


asyncio.run(main())
```

## Likely follow-ups

- What happens if an exception is raised inside the `finally` block of an async generator?
- How does Starlette's `StreamingResponse` propagate cancellation to the underlying generator?

---

[← Q0864](../../batch_09_genai_services_fastapi/0864_content_negotiation_supporting_both_json_completion_and_sse/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0866 →](../../batch_09_genai_services_fastapi/0866_fastapi_dependency_overrides_for_integration_testing/README.md)

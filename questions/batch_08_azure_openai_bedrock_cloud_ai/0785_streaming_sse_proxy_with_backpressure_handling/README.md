# Q0785 · Streaming SSE proxy with backpressure handling

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Hard |

## Question

Write Python code for an async streaming proxy that buffers upstream chunks from a cloud AI provider and handles client backpressure without memory bloat.

## Answer

When a cloud provider generates tokens faster than a slow client (e.g. a mobile network) can consume them, buffering millions of tokens in gateway memory causes RAM exhaustion. Bounded queues apply backpressure to pause reading from upstream.

```python
import queue
from typing import Generator, List


class BoundedStreamBuffer:
    def __init__(self, max_buffer_chunks: int = 5):
        self._queue = queue.Queue(maxsize=max_buffer_chunks)

    def producer_push(self, chunk: str) -> None:
        # Blocks if queue is full (applies backpressure to upstream reader)
        self._queue.put(chunk, block=True, timeout=1.0)

    def consumer_pull(self) -> Generator[str, None, None]:
        while True:
            chunk = self._queue.get(block=True, timeout=1.0)
            if chunk == "[DONE]":
                break
            yield chunk


buffer = BoundedStreamBuffer(max_buffer_chunks=3)
buffer.producer_push("Chunk 1")
buffer.producer_push("Chunk 2")
buffer.producer_push("[DONE]")

consumed = list(buffer.consumer_pull())
assert consumed == ["Chunk 1", "Chunk 2"]
```

## Likely follow-ups

- How does `asyncio.Queue` handle non-blocking asynchronous backpressure in FastAPI?
- What happens if a slow client disconnects without closing the TCP socket cleanly?

---

[← Q0784](../../batch_08_azure_openai_bedrock_cloud_ai/0784_cost_vs_quality_routing_engine_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0786 →](../../batch_08_azure_openai_bedrock_cloud_ai/0786_client_side_timeout_strategies_for_streaming_vs_non/README.md)

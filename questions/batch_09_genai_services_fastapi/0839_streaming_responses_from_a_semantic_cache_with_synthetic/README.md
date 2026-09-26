# Q0839 · Streaming responses from a semantic cache with synthetic chunk delays

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Medium |

## Question

When returning a cached response over Server-Sent Events (SSE), dumping 2,000 tokens instantaneously can break UI renderers expecting a typing cadence. Write Python code simulating synthetic token streaming.

## Answer

Frontend chat interfaces often rely on smooth token streaming for animation, scroll-anchor tracking, and markdown rendering. Returning a full cached document in a single instantaneous frame can cause UI jank.

A synthetic streaming generator chunks the cached string into small token-like slices (e.g. 2-4 words) and yields them with micro-delays (e.g. 10ms) or instantly if high throughput is prioritized.

```python
import asyncio
from typing import AsyncGenerator, List


async def stream_cached_response(
    cached_text: str, chunk_size: int = 3, delay_sec: float = 0.001
) -> AsyncGenerator[str, None]:
    '''Simulates streaming tokens from a cached response.'''
    words = cached_text.split(" ")
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        if i + chunk_size < len(words):
            chunk += " "
        yield f"data: {chunk}\n\n"
        if delay_sec > 0:
            await asyncio.sleep(delay_sec)
    yield "data: [DONE]\n\n"


async def main():
    text = "The Federal Reserve raised target rates by 25 basis points."
    chunks = []
    async for item in stream_cached_response(text, chunk_size=3, delay_sec=0.001):
        chunks.append(item)
    assert len(chunks) >= 3
    assert chunks[-1] == "data: [DONE]\n\n"
    assert "Federal Reserve" in chunks[0]


asyncio.run(main())
```

## Likely follow-ups

- When should you disable synthetic delay (e.g. automated API clients vs human interactive UIs)?
- How does synthetic streaming impact overall server thread/event loop capacity?

---

[← Q0838](../../batch_09_genai_services_fastapi/0838_estimating_and_tracking_prompt_token_savings_and_cache_roi/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0840 →](../../batch_09_genai_services_fastapi/0840_sensitive_data_leakage_prevention_in_shared_enterprise/README.md)

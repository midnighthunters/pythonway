# Q0836 · Cache stampede prevention with distributed locks (Redlock)

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Hard |

## Question

Explain the cache stampede (thundering herd) problem when an expensive LLM response expires, and write Python code simulating single-flight request coalescing.

## Answer

When a popular cached item expires under high traffic (e.g. 500 requests/second querying market open commentary), hundreds of concurrent requests experience a cache miss simultaneously. They all invoke the upstream LLM, causing quota exhaustion, spike in compute bills, and degraded response times.

Solutions:
1. **Single-flight / Request Coalescing**: Ensuring only one worker invokes the LLM while all other concurrent requests await its result.
2. **Probabilistic Early Expiration (XFetch algorithm)**: Recomputing the value asynchronously before it officially expires.

```python
import asyncio
from typing import Dict, Optional


class SingleFlightLLMCaller:
    def __init__(self):
        self.cache: Dict[str, str] = {}
        self.in_flight_tasks: Dict[str, asyncio.Future] = {}

    async def get_or_call(self, prompt: str) -> str:
        # Cache hit
        if prompt in self.cache:
            return self.cache[prompt]

        # Check if already being computed by another request
        if prompt in self.in_flight_tasks:
            # Await the existing computation without calling LLM again
            return await self.in_flight_tasks[prompt]

        # First request creates the future
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.in_flight_tasks[prompt] = future

        try:
            # Simulate expensive LLM call (50ms)
            await asyncio.sleep(0.05)
            result = f"LLM Output for: {prompt}"
            self.cache[prompt] = result
            future.set_result(result)
            return result
        finally:
            if prompt in self.in_flight_tasks:
                del self.in_flight_tasks[prompt]


async def main():
    caller = SingleFlightLLMCaller()
    # 5 concurrent requests arrive at the exact same moment
    results = await asyncio.gather(
        caller.get_or_call("Market Summary"),
        caller.get_or_call("Market Summary"),
        caller.get_or_call("Market Summary"),
        caller.get_or_call("Market Summary"),
        caller.get_or_call("Market Summary"),
    )
    assert len(results) == 5
    assert all(r == "LLM Output for: Market Summary" for r in results)


asyncio.run(main())
```

## Likely follow-ups

- What happens if the single-flight worker task crashes before setting the future result?
- How does Redis distributed lock (Redlock) work across multiple physical server nodes?

---

[← Q0835](../../batch_09_genai_services_fastapi/0835_handling_temperature_and_non_determinism_in_semantic_cache/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0837 →](../../batch_09_genai_services_fastapi/0837_negative_caching_and_error_response_caching_mitigation/README.md)

# Q0900 · Complete production architecture review: end-to-end design of an enterprise GenAI service

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Hard |

## Question

Provide an end-to-end architectural synthesis of an enterprise-grade GenAI microservice in Python/FastAPI, integrating security, rate limiting, semantic caching, queuing, and streaming.

## Answer

A production enterprise GenAI microservice encompasses a multi-layered pipeline:

1. **Perimeter & Security**: Corporate forward proxy, mTLS, OAuth2/JWT auth, Pydantic v2 input sanitization, and security headers.
2. **Traffic Management**: Redis sliding-window rate limiting (RPM/TPM), tenant quota budgeting, and single-flight request deduplication.
3. **In-Memory Acceleration**: L1 LRU and L2 Redis semantic vector cache, returning cached responses with synthetic SSE chunk cadence when applicable.
4. **Execution Engine**:
   - **Fast Interactive Calls**: Asynchronous streaming over SSE with TTFT and ITL telemetry.
   - **Long-Running Agents**: 202 Accepted response, offloading tasks to ARQ / Celery workers with claim-check S3 storage and SQS visibility heartbeats.
5. **State & Observability**: DynamoDB/Cosmos DB partitioned thread history, Prometheus metrics `/metrics`, and OpenTelemetry distributed traces.

```python
import asyncio
from typing import AsyncGenerator, Dict


class EnterpriseGenAIServiceOrchestrator:
    def __init__(self):
        self.cache: Dict[str, str] = {}
        self.metrics = {"requests": 0, "cache_hits": 0}

    async def handle_chat_request(self, tenant_id: str, prompt: str) -> AsyncGenerator[str, None]:
        self.metrics["requests"] += 1

        # 1. Cache check
        if prompt in self.cache:
            self.metrics["cache_hits"] += 1
            yield f"data: [CACHED] {self.cache[prompt]}\n\n"
            yield "data: [DONE]\n\n"
            return

        # 2. Simulated LLM generation
        reply = f"Analysis for tenant {tenant_id}: Completed."
        self.cache[prompt] = reply

        # 3. Stream response chunks
        for word in reply.split():
            yield f"data: {word}\n\n"
            await asyncio.sleep(0.001)
        yield "data: [DONE]\n\n"


async def main():
    service = EnterpriseGenAIServiceOrchestrator()

    # First request: cache miss, streams generated tokens
    stream1 = [chunk async for chunk in service.handle_chat_request("dept_fx", "VaR Summary")]
    assert len(stream1) >= 4
    assert service.metrics["cache_hits"] == 0

    # Second request: cache hit
    stream2 = [chunk async for chunk in service.handle_chat_request("dept_fx", "VaR Summary")]
    assert "[CACHED]" in stream2[0]
    assert service.metrics["cache_hits"] == 1


asyncio.run(main())
```

## Likely follow-ups

- How do you conduct end-to-end load testing (Locust, k6) to simulate 10,000 concurrent streaming connections?
- How does technology controls agenda (TCA) compliance mandate audit trails for all LLM inputs and outputs?

---

[← Q0899](../../batch_09_genai_services_fastapi/0899_disaster_recovery_multi_region_active_passive_failover_and/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md)

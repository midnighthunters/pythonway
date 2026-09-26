# Q0846 · Asynchronous usage event publishing to Kafka for enterprise billing

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Medium |

## Question

Write Python code implementing an asynchronous usage event emitter that publishes token usage and cost records to a mock message bus without adding latency to the user response.

## Answer

To avoid adding 20-50ms latency to every user chat response, billing and telemetry records should be decoupled from the synchronous HTTP request/response cycle. Emitting usage events asynchronously to Kafka, AWS Kinesis, or Azure Event Hubs guarantees fire-and-forget delivery.

```python
import asyncio
from datetime import datetime, timezone
from typing import Dict, List


class MockKafkaProducer:
    def __init__(self):
        self.messages: List[Dict] = []

    async def send_and_wait(self, topic: str, value: Dict) -> None:
        await asyncio.sleep(0.005)  # Simulate network hop
        self.messages.append({"topic": topic, "value": value})


class TelemetryBillingEmitter:
    def __init__(self, producer: MockKafkaProducer):
        self.producer = producer

    def emit_usage_background(
        self, tenant_id: str, model: str, in_tokens: int, out_tokens: int, cost_usd: float
    ) -> None:
        payload = {
            "tenant_id": tenant_id,
            "model": model,
            "input_tokens": in_tokens,
            "output_tokens": out_tokens,
            "cost_usd": cost_usd,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        # Fire-and-forget task on current event loop
        asyncio.create_task(self.producer.send_and_wait("llm-suite-billing", payload))


async def main():
    producer = MockKafkaProducer()
    emitter = TelemetryBillingEmitter(producer)

    emitter.emit_usage_background("dept_equities", "gpt-4o", 1200, 450, 0.0075)
    assert len(producer.messages) == 0  # Still executing in background

    await asyncio.sleep(0.02)  # Yield to event loop
    assert len(producer.messages) == 1
    assert producer.messages[0]["value"]["tenant_id"] == "dept_equities"


asyncio.run(main())
```

## Likely follow-ups

- What happens if the service crashes before background asyncio tasks finish sending?
- How does Kafka partitioning by `tenant_id` guarantee strict ordering of billing events?

---

[← Q0845](../../batch_09_genai_services_fastapi/0845_finops_cost_metering_calculating_usd_cost_per_request_by/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0847 →](../../batch_09_genai_services_fastapi/0847_http_429_retry_after_headers_and_client_cooperative_backoff/README.md)

# Q0884 · Throttling worker consumption to match downstream cloud API limits

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code implementing a token-rate throttled queue consumer that regulates dequeue rate to stay within downstream provider Tier-2 limits (e.g. 10 requests per second).

## Answer

If 50 Celery workers concurrently pull tasks from SQS and hammer Azure OpenAI at 50 requests/second, the upstream service will throttle all workers with HTTP 429 errors. Regulating the consumer dequeue rate maintains smooth throughput without triggering errors.

```python
import time


class RateThrottledConsumer:
    def __init__(self, max_per_second: float):
        self.min_interval = 1.0 / max_per_second
        self.last_pull_time = 0.0

    def wait_for_slot(self, current_time: float) -> float:
        elapsed = current_time - self.last_pull_time
        if elapsed < self.min_interval:
            sleep_needed = self.min_interval - elapsed
            self.last_pull_time = current_time + sleep_needed
            return sleep_needed
        else:
            self.last_pull_time = current_time
            return 0.0


consumer = RateThrottledConsumer(max_per_second=10.0)  # 1 request per 0.1s

t0 = 100.0
# Request 1: Immediate slot
sleep1 = consumer.wait_for_slot(t0)
assert sleep1 == 0.0

# Request 2 arrives 0.02s later: must wait 0.08s
sleep2 = consumer.wait_for_slot(t0 + 0.02)
assert round(sleep2, 3) == 0.080
```

## Likely follow-ups

- How does Redis-based distributed token bucket synchronization coordinate rate limits across 50 separate worker instances?
- What is the difference between client-side queue throttling and server-side HTTP 429 backoff?

---

[← Q0883](../../batch_09_genai_services_fastapi/0883_exactly_once_processing_versus_at_least_once_processing_in/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0885 →](../../batch_09_genai_services_fastapi/0885_testing_async_workers_in_isolation_with_mocks_and_test/README.md)

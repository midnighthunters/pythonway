# Q0855 · Measuring Time to First Token and Inter-Token Latency in middleware

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI streaming | Medium |

## Question

Write Python code tracking Time to First Token (TTFT) and Inter-Token Latency (ITL) during an SSE streaming completion, recording metrics for APM telemetry.

## Answer

In GenAI user experience:
- **TTFT (Time to First Token)**: Time from HTTP request arrival until the first token chunk is yielded to the client. This drives perceived responsiveness.
- **ITL (Inter-Token Latency)**: Average and P95 time between consecutive tokens. High ITL causes perceptible stuttering in chat UIs.

```python
import time
from typing import List


class StreamingMetricsTracker:
    def __init__(self):
        self.start_time = time.time()
        self.first_token_time = None
        self.last_token_time = None
        self.token_intervals: List[float] = []
        self.token_count = 0

    def record_chunk(self) -> None:
        now = time.time()
        self.token_count += 1
        if self.first_token_time is None:
            self.first_token_time = now
            self.last_token_time = now
        else:
            interval = now - self.last_token_time
            self.token_intervals.append(interval)
            self.last_token_time = now

    def get_summary(self) -> dict:
        ttft = (self.first_token_time - self.start_time) if self.first_token_time else 0.0
        avg_itl = (sum(self.token_intervals) / len(self.token_intervals)) if self.token_intervals else 0.0
        return {
            "total_tokens": self.token_count,
            "ttft_ms": round(ttft * 1000, 2),
            "avg_itl_ms": round(avg_itl * 1000, 2),
        }


tracker = StreamingMetricsTracker()
# Simulate first token arrival after 20ms
time.sleep(0.02)
tracker.record_chunk()

# Simulate subsequent tokens
for _ in range(5):
    time.sleep(0.005)
    tracker.record_chunk()

metrics = tracker.get_summary()
assert metrics["total_tokens"] == 6
assert metrics["ttft_ms"] >= 15.0
assert metrics["avg_itl_ms"] >= 3.0
```

## Likely follow-ups

- What are industry standard target SLAs for TTFT in interactive financial assistants (typically < 800ms)?
- How do prompt caching and speculative decoding drastically reduce TTFT?

---

[← Q0854](../../batch_09_genai_services_fastapi/0854_streaming_backpressure_handling_when_slow_clients_cannot/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0856 →](../../batch_09_genai_services_fastapi/0856_structured_json_logging_middleware_with_correlation_ids/README.md)

# Q0841 · Sliding-window rate limiting middleware using Redis Lua scripts

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Hard |

## Question

Explain the sliding-window log/counter rate limiting algorithm and write Python code simulating atomic sliding-window rate limiting for GenAI API requests.

## Answer

Fixed-window rate limiters suffer from the "boundary burst" flaw: a user allowed 100 requests/minute can send 100 requests at 00:59 and 100 requests at 01:00, effectively sending 200 requests within two seconds.

A **sliding-window counter** uses Redis sorted sets (`ZSET`) where:
1. Each request adds a timestamp as score and member.
2. Elements older than `now - window_size` are purged (`ZREMRANGEBYSCORE`).
3. Total remaining elements are counted (`ZCARD`).
4. If count <= limit, allow; else reject with HTTP 429.

```python
import time
from typing import Dict, List


class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window = window_seconds
        # Simulates Redis ZSET: client_id -> list of float timestamps
        self.client_timestamps: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str, current_time: float) -> bool:
        if client_id not in self.client_timestamps:
            self.client_timestamps[client_id] = []

        timestamps = self.client_timestamps[client_id]
        # Step 1: Remove timestamps outside current sliding window
        cutoff = current_time - self.window
        self.client_timestamps[client_id] = [t for t in timestamps if t > cutoff]
        timestamps = self.client_timestamps[client_id]

        # Step 2: Check limit
        if len(timestamps) < self.limit:
            timestamps.append(current_time)
            return True
        return False


limiter = SlidingWindowRateLimiter(limit=3, window_seconds=1.0)
now = 100.0

assert limiter.is_allowed("client_A", now + 0.1) is True
assert limiter.is_allowed("client_A", now + 0.2) is True
assert limiter.is_allowed("client_A", now + 0.3) is True
# Exceeds limit of 3 within 1.0s window
assert limiter.is_allowed("client_A", now + 0.4) is False

# After window elapses, new requests are allowed
assert limiter.is_allowed("client_A", now + 1.2) is True
```

## Likely follow-ups

- Why must this operation be executed as a Redis Lua script or Redis transaction?
- How does sliding-window counter approximate memory usage compared to sliding-window log?

---

[← Q0840](../../batch_09_genai_services_fastapi/0840_sensitive_data_leakage_prevention_in_shared_enterprise/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0842 →](../../batch_09_genai_services_fastapi/0842_token_bucket_algorithm_for_managing_llm_token_rate_limits/README.md)

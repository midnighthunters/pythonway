# Q0745 · Per-tenant rate limiting with sliding window in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Implement a sliding-window rate limiter in Python that enforces requests-per-minute (RPM) quotas per enterprise tenant ID.

## Answer

```python
import time
from typing import Dict, List


class SlidingWindowRateLimiter:
    def __init__(self, max_rpm: int = 5, window_seconds: float = 1.0):
        self.max_rpm = max_rpm
        self.window_seconds = window_seconds
        self._tenant_timestamps: Dict[str, List[float]] = {}

    def is_allowed(self, tenant_id: str) -> bool:
        now = time.time()
        if tenant_id not in self._tenant_timestamps:
            self._tenant_timestamps[tenant_id] = []

        # Evict timestamps older than the sliding window
        cutoff = now - self.window_seconds
        valid_stamps = [t for t in self._tenant_timestamps[tenant_id] if t > cutoff]
        self._tenant_timestamps[tenant_id] = valid_stamps

        if len(valid_stamps) < self.max_rpm:
            self._tenant_timestamps[tenant_id].append(now)
            return True
        return False


limiter = SlidingWindowRateLimiter(max_rpm=2, window_seconds=0.1)
assert limiter.is_allowed("desk-1") is True
assert limiter.is_allowed("desk-1") is True
assert limiter.is_allowed("desk-1") is False  # Limit reached

# Different tenant is unaffected
assert limiter.is_allowed("desk-2") is True

# After window elapses, capacity resets
time.sleep(0.12)
assert limiter.is_allowed("desk-1") is True
```

## Likely follow-ups

- Why is sliding window superior to fixed window counters for burst protection?
- How is this pattern implemented in distributed systems using Redis sorted sets (ZADD / ZREMRANGEBYSCORE)?

---

[← Q0744](../../batch_08_azure_openai_bedrock_cloud_ai/0744_implementing_a_stateful_circuit_breaker_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0746 →](../../batch_08_azure_openai_bedrock_cloud_ai/0746_request_deduplication_for_identical_in_flight_prompts/README.md)

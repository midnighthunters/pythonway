# Q0842 · Token bucket algorithm for managing LLM token rate limits (TPM)

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Medium |

## Question

Write Python code implementing the Token Bucket algorithm to enforce Tokens-Per-Minute (TPM) limits alongside Requests-Per-Minute (RPM) limits in FastAPI services.

## Answer

Cloud LLM providers enforce dual constraints:
1. **RPM (Requests Per Minute)**: Total number of HTTP API calls.
2. **TPM (Tokens Per Minute)**: Total combined prompt + completion tokens consumed.

The Token Bucket algorithm continuously refills tokens at a fixed rate up to bucket capacity. Incoming requests consume N tokens; if insufficient tokens exist, the request is throttled.

```python
import time


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = None

    def _refill(self, now: float) -> None:
        if self.last_refill is None:
            self.last_refill = now
            return
        elapsed = max(0.0, now - self.last_refill)
        refill_amount = elapsed * self.refill_rate
        self.tokens = min(float(self.capacity), self.tokens + refill_amount)
        self.last_refill = now

    def consume(self, requested_tokens: int, now: float) -> bool:
        self._refill(now)
        if self.tokens >= requested_tokens:
            self.tokens -= requested_tokens
            return True
        return False


limiter = TokenBucketRateLimiter(capacity=1000, refill_rate_per_sec=100.0)
t0 = 1000.0

# Request 1: Consumes 600 tokens
assert limiter.consume(600, t0) is True
assert round(limiter.tokens) == 400

# Request 2: Wants 500 tokens immediately (only 400 available)
assert limiter.consume(500, t0) is False

# After 2 seconds, 200 tokens have refilled (400 + 200 = 600)
assert limiter.consume(500, t0 + 2.0) is True
```

## Likely follow-ups

- What is the difference between Token Bucket and Leaky Bucket algorithms?
- How do you estimate prompt tokens before sending the request to the upstream LLM?

---

[← Q0841](../../batch_09_genai_services_fastapi/0841_sliding_window_rate_limiting_middleware_using_redis_lua/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0843 →](../../batch_09_genai_services_fastapi/0843_tenant_based_quota_enforcement_and_tiered_subscription_rate/README.md)

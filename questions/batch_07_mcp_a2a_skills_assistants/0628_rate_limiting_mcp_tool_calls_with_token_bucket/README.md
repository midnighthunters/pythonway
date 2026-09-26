# Q0628 · Rate limiting MCP tool calls with token bucket

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Implement a Token Bucket rate limiter in Python to throttle outgoing tool calls to an expensive or rate-limited MCP server.

## Answer

Downstream enterprise systems often enforce strict QPS (queries per second) quotas. An MCP client or middleware layer must rate-limit tool calls to prevent 429 throttling.

```python
import time
from typing import Optional


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def acquire(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_sec=10.0)
assert limiter.acquire() is True
assert limiter.acquire() is True
assert limiter.acquire() is False
time.sleep(0.15)
assert limiter.acquire() is True
```

## Likely follow-ups

- What is the difference between client-side rate limiting and server-side backpressure?
- How should rate-limit failures be communicated back to the LLM agent?

---

[← Q0627](../../batch_07_mcp_a2a_skills_assistants/0627_handling_parallel_tool_calls_across_multiple_mcp_servers/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0629 →](../../batch_07_mcp_a2a_skills_assistants/0629_caching_idempotent_mcp_tool_call_responses/README.md)

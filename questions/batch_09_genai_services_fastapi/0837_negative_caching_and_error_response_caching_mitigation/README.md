# Q0837 · Negative caching and error response caching mitigation

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Medium |

## Question

What is negative caching, when is it useful in GenAI services, and write Python code implementing short-TTL negative caching for downstream model errors.

## Answer

Negative caching stores failure responses (e.g. 404 Not Found, 400 Bad Request, or invalid stock ticker symbol) to prevent malicious or malformed queries from repeatedly hammering downstream vector stores or LLM endpoints.

However, downstream transient errors (HTTP 500, 503, or 429 Rate Limited) must **never** be cached long-term; they should either not be cached or cached with a tiny TTL (e.g. 2 seconds) to avoid poisoning the cache during temporary outages.

```python
import time
from typing import Dict, Optional, Tuple


class ErrorAwareCache:
    def __init__(self, success_ttl: int = 3600, negative_ttl: int = 5):
        self.success_ttl = success_ttl
        self.negative_ttl = negative_ttl
        # Key -> (value, is_error, expires_at)
        self.store: Dict[str, Tuple[str, bool, float]] = {}

    def set(self, key: str, val: str, is_error: bool) -> None:
        ttl = self.negative_ttl if is_error else self.success_ttl
        self.store[key] = (val, is_error, time.time() + ttl)

    def get(self, key: str) -> Optional[Tuple[str, bool]]:
        if key not in self.store:
            return None
        val, is_err, expires_at = self.store[key]
        if time.time() > expires_at:
            del self.store[key]
            return None
        return val, is_err


cache = ErrorAwareCache(success_ttl=100, negative_ttl=2)
# Negative cache: Unknown ticker
cache.set("ticker:INVALID", "Symbol not found in NYSE database", is_error=True)

# Immediate read
res = cache.get("ticker:INVALID")
assert res is not None
assert res[1] is True  # is_error flag

# Simulate expiration of negative cache
cache.store["ticker:INVALID"] = (res[0], res[1], time.time() - 1)
assert cache.get("ticker:INVALID") is None
```

## Likely follow-ups

- What security vulnerability arises if an attacker can force negative cache poisoning for valid queries?
- How do you differentiate permanent 4xx errors from transient 5xx errors in caching middleware?

---

[← Q0836](../../batch_09_genai_services_fastapi/0836_cache_stampede_prevention_with_distributed_locks_redlock/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0838 →](../../batch_09_genai_services_fastapi/0838_estimating_and_tracking_prompt_token_savings_and_cache_roi/README.md)

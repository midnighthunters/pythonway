# Q0835 · Handling temperature and non-determinism in semantic cache keys

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Medium |

## Question

Explain how LLM sampling parameters (temperature, top_p, presence_penalty) affect caching policies, and write Python code implementing parameter-aware cache lookups.

## Answer

When `temperature > 0.0`, responses are expected to vary across requests to foster creative or varied outputs. Returning a cached response for `temperature = 1.0` defeats the caller's explicit intent for stochastic sampling.

Best practice rules:
1. `temperature == 0.0`: Aggressive caching permitted (deterministic output).
2. `0.0 < temperature <= 0.3`: Caching allowed for factual / corporate Q&A where determinism is desired despite slight sampling noise.
3. `temperature > 0.5`: Caching should be disabled or explicitly bypassed via headers (e.g. `Cache-Control: no-cache`).

```python
from typing import Dict, Optional


class SamplingAwareCache:
    def __init__(self, max_cachable_temp: float = 0.2):
        self.max_cachable_temp = max_cachable_temp
        self.cache: Dict[str, str] = {}

    def get_response(self, prompt: str, temperature: float) -> Optional[str]:
        if temperature > self.max_cachable_temp:
            return None  # Bypass cache for non-deterministic requests
        key = f"{prompt}:{temperature:.2f}"
        return self.cache.get(key)

    def set_response(self, prompt: str, temperature: float, response: str) -> None:
        if temperature <= self.max_cachable_temp:
            key = f"{prompt}:{temperature:.2f}"
            self.cache[key] = response


cache = SamplingAwareCache(max_cachable_temp=0.2)
cache.set_response("Define Liquidity Coverage Ratio", 0.0, "LCR is a Basel III requirement...")

# Cachable request (temp = 0.0)
assert cache.get_response("Define Liquidity Coverage Ratio", 0.0) is not None

# Non-cachable request (temp = 0.8)
assert cache.get_response("Define Liquidity Coverage Ratio", 0.8) is None
```

## Likely follow-ups

- How does `seed` parameter in modern OpenAI/Bedrock models interact with caching?
- What HTTP header should clients send to force a cache refresh (`no-cache`)?

---

[← Q0834](../../batch_09_genai_services_fastapi/0834_multi_tier_caching_architecture_l1_in_memory_lru_and_l2/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0836 →](../../batch_09_genai_services_fastapi/0836_cache_stampede_prevention_with_distributed_locks_redlock/README.md)

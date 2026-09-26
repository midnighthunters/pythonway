# Q0851 · Adaptive rate limiting based on upstream error rates and response latency

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Hard |

## Question

Explain how adaptive rate limiting protects GenAI microservices during upstream degradation, and write Python code implementing an adaptive limit adjuster based on sliding-window error rates.

## Answer

Static rate limits cannot react when upstream providers (Azure OpenAI, Anthropic, Bedrock) suffer partial degradation, increased latency, or throttling (HTTP 429). Adaptive rate limiting dynamically reduces the allowed concurrency when the upstream error rate exceeds a safety threshold (e.g. > 5% errors) or P95 latency spikes, and gently scales capacity back up as healthy responses return (additive-increase/multiplicative-decrease, AIMD).

```python
from typing import List


class AdaptiveRateLimiter:
    def __init__(self, min_concurrency: int = 2, max_concurrency: int = 20):
        self.min_concurrency = min_concurrency
        self.max_concurrency = max_concurrency
        self.current_limit = max_concurrency
        self.window_results: List[bool] = []  # True = success, False = error
        self.window_size = 20

    def record_result(self, success: bool) -> None:
        self.window_results.append(success)
        if len(self.window_results) > self.window_size:
            self.window_results.pop(0)
        self._adjust_limit()

    def _adjust_limit(self) -> None:
        if len(self.window_results) < 10:
            return  # Warm-up phase

        error_count = self.window_results.count(False)
        error_rate = error_count / len(self.window_results)

        if error_rate > 0.15:
            # Multiplicative decrease (back off by 30%)
            self.current_limit = max(self.min_concurrency, int(self.current_limit * 0.7))
        elif error_rate < 0.05 and self.current_limit < self.max_concurrency:
            # Additive increase (+1 slot)
            self.current_limit = min(self.max_concurrency, self.current_limit + 1)


limiter = AdaptiveRateLimiter(min_concurrency=2, max_concurrency=10)
# Simulate 15 consecutive upstream failures (e.g. Azure OpenAI 503/429 spikes)
for _ in range(15):
    limiter.record_result(success=False)

assert limiter.current_limit < 10
assert limiter.current_limit >= 2
```

## Likely follow-ups

- How does the TCP congestion control algorithm (TCP Vegas / BBR) inspire API gateway rate limits?
- How do you prevent flapping (rapid oscillation) between throttling and un-throttling?

---

[← Q0850](../../batch_09_genai_services_fastapi/0850_circuit_breaker_pattern_for_downstream_llm_provider_outages/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0852 →](../../batch_09_genai_services_fastapi/0852_graceful_degradation_and_fallback_to_smaller_models_under/README.md)

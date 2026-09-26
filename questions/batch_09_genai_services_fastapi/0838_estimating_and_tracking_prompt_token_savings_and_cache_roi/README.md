# Q0838 · Estimating and tracking prompt token savings and cache ROI in production

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Semantic caching | Easy |

## Question

Write Python code to track and aggregate token savings, financial cost savings, and latency reductions achieved through response caching in an enterprise GenAI service.

## Answer

Demonstrating Return on Investment (ROI) for caching infrastructure requires tracking:
1. Total cache hits vs misses (Hit Rate).
2. Input and output tokens averted from LLM calls.
3. Cumulative USD saved based on provider pricing cards.
4. Cumulative milliseconds of user waiting time saved.

```python
class CacheTelemetryTracker:
    def __init__(self, price_per_1k_input: float = 0.005, price_per_1k_output: float = 0.015):
        self.p_in = price_per_1k_input
        self.p_out = price_per_1k_output
        self.total_requests = 0
        self.hits = 0
        self.tokens_saved_input = 0
        self.tokens_saved_output = 0
        self.latency_saved_ms = 0.0

    def record_hit(self, in_tokens: int, out_tokens: int, estimated_llm_latency_ms: float) -> None:
        self.total_requests += 1
        self.hits += 1
        self.tokens_saved_input += in_tokens
        self.tokens_saved_output += out_tokens
        self.latency_saved_ms += estimated_llm_latency_ms

    def record_miss(self) -> None:
        self.total_requests += 1

    def get_summary(self) -> dict:
        hit_rate = (self.hits / self.total_requests) if self.total_requests > 0 else 0.0
        cost_saved = (self.tokens_saved_input / 1000 * self.p_in) + (self.tokens_saved_output / 1000 * self.p_out)
        return {
            "hit_rate_pct": round(hit_rate * 100, 2),
            "cost_saved_usd": round(cost_saved, 4),
            "tokens_saved": self.tokens_saved_input + self.tokens_saved_output,
            "latency_saved_sec": round(self.latency_saved_ms / 1000, 2),
        }


tracker = CacheTelemetryTracker(price_per_1k_input=0.005, price_per_1k_output=0.015)
tracker.record_miss()
tracker.record_hit(in_tokens=500, out_tokens=200, estimated_llm_latency_ms=1200.0)
tracker.record_hit(in_tokens=300, out_tokens=150, estimated_llm_latency_ms=900.0)

summary = tracker.get_summary()
assert summary["hit_rate_pct"] == 66.67
assert summary["tokens_saved"] == 1150
assert summary["cost_saved_usd"] > 0.008
assert summary["latency_saved_sec"] == 2.1
```

## Likely follow-ups

- How do you expose these metrics to Prometheus for Grafana dashboard visualization?
- What are typical enterprise cache-hit rates for customer-facing vs internal employee GenAI bots?

---

[← Q0837](../../batch_09_genai_services_fastapi/0837_negative_caching_and_error_response_caching_mitigation/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0839 →](../../batch_09_genai_services_fastapi/0839_streaming_responses_from_a_semantic_cache_with_synthetic/README.md)

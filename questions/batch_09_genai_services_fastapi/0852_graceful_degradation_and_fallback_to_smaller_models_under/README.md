# Q0852 · Graceful degradation and fallback to smaller models under heavy load

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Medium |

## Question

Write Python code implementing an automated fallback router in FastAPI that degrades from a primary frontier model (GPT-4o) to a lightweight fast model (GPT-4o-mini) when the primary is throttled or errors.

## Answer

In critical enterprise banking applications, returning a slightly less detailed answer is far superior to dropping the user's connection with an HTTP 500 error. The fallback router catches 429/503 errors from the primary model and retries against a backup deployment.

```python
from typing import Optional


class MockModelClient:
    def __init__(self, model_name: str, will_fail: bool = False):
        self.model_name = model_name
        self.will_fail = will_fail

    def generate(self, prompt: str) -> str:
        if self.will_fail:
            raise ConnectionError(f"HTTP 429: {self.model_name} rate limit reached")
        return f"Response from {self.model_name}: {prompt}"


def generate_with_fallback(prompt: str, primary: MockModelClient, fallback: MockModelClient) -> dict:
    try:
        reply = primary.generate(prompt)
        return {"model_used": primary.model_name, "content": reply, "degraded": False}
    except Exception:
        # Fallback to secondary smaller/cheaper model
        reply = fallback.generate(prompt)
        return {"model_used": fallback.model_name, "content": reply, "degraded": True}


primary = MockModelClient("gpt-4o", will_fail=True)
fallback = MockModelClient("gpt-4o-mini", will_fail=False)

result = generate_with_fallback("Calculate portfolio beta", primary, fallback)
assert result["degraded"] is True
assert result["model_used"] == "gpt-4o-mini"
assert "Calculate portfolio beta" in result["content"]
```

## Likely follow-ups

- What user experience cues or headers should inform the client that fallback degradation occurred?
- How do you prevent fallback models from also becoming overloaded during major primary outages?

---

[← Q0851](../../batch_09_genai_services_fastapi/0851_adaptive_rate_limiting_based_on_upstream_error_rates_and/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0853 →](../../batch_09_genai_services_fastapi/0853_request_deduplication_middleware_for_idempotent_chat/README.md)

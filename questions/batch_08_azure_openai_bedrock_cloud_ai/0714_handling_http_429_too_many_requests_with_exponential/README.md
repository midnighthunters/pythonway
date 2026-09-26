# Q0714 · Handling HTTP 429 Too Many Requests with exponential backoff and jitter

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Write Python code implementing an asynchronous retry handler with exponential backoff and Full Jitter for cloud LLM API calls returning HTTP 429.

## Answer

When calling cloud LLM endpoints (Azure OpenAI or AWS Bedrock), traffic spikes trigger HTTP 429 rate limits. Using fixed retries causes synchronized "thundering herd" spikes. Full Jitter spreads retry intervals randomly across the backoff window.

Formula (Full Jitter):
`sleep = random.uniform(0, min(max_backoff, base_backoff * (2 ** attempt)))`

```python
import random
import time
from typing import Any, Callable, Dict


class RateLimitRetryHandler:
    def __init__(self, max_retries: int = 3, base_backoff: float = 0.5, max_backoff: float = 4.0):
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff
        self.sleep_durations = []

    def execute(self, api_fn: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                return api_fn()
            except Exception as exc:
                if "429" not in str(exc) or attempt == self.max_retries:
                    raise exc

                # Compute exponential backoff with full jitter
                backoff_cap = min(self.max_backoff, self.base_backoff * (2 ** attempt))
                jittered_sleep = random.uniform(0.01, backoff_cap)
                self.sleep_durations.append(jittered_sleep)
                time.sleep(jittered_sleep)


# Simulated flaky endpoint
attempts = 0


def flaky_call():
    global attempts
    attempts += 1
    if attempts < 3:
        raise ConnectionError("HTTP 429 Too Many Requests: Rate limit exceeded")
    return {"status": "success", "result": "Model output"}


handler = RateLimitRetryHandler(max_retries=4, base_backoff=0.1, max_backoff=1.0)
res = handler.execute(flaky_call)

assert res["status"] == "success"
assert len(handler.sleep_durations) == 2  # Retried twice
assert all(d <= 1.0 for d in handler.sleep_durations)
```

## Likely follow-ups

- Why is Full Jitter mathematically superior to Equal Jitter or Decorrelated Jitter?
- How should the `Retry-After` HTTP response header be prioritized over calculated backoff?

---

[← Q0713](../../batch_08_azure_openai_bedrock_cloud_ai/0713_amazon_bedrock_agents_and_agentcore/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0715 →](../../batch_08_azure_openai_bedrock_cloud_ai/0715_multi_provider_fallback_router_azure_openai_to_aws_bedrock/README.md)

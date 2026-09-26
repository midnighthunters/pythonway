# Q0795 · Rate limit header parser: Retry-After, X-RateLimit-Reset

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Write Python code that parses HTTP response headers (`Retry-After`, `x-ratelimit-reset-requests`) and calculates exact wait durations in seconds.

## Answer

```python
from typing import Dict


class RateLimitHeaderParser:
    @staticmethod
    def parse_wait_seconds(headers: Dict[str, str], default_wait: float = 1.0) -> float:
        # Check standard Retry-After (seconds or HTTP date)
        if "Retry-After" in headers:
            val = headers["Retry-After"]
            try:
                return max(0.1, float(val))
            except ValueError:
                pass  # If HTTP date format, fallback or parse date

        # Check Azure / OpenAI specific header
        if "x-ratelimit-reset-requests" in headers:
            val = headers["x-ratelimit-reset-requests"]
            # e.g. "15s" or "200ms"
            if val.endswith("ms"):
                return max(0.05, float(val[:-2]) / 1000.0)
            if val.endswith("s"):
                return max(0.1, float(val[:-1]))

        return default_wait


h1 = {"Retry-After": "3.5"}
assert RateLimitHeaderParser.parse_wait_seconds(h1) == 3.5

h2 = {"x-ratelimit-reset-requests": "250ms"}
assert RateLimitHeaderParser.parse_wait_seconds(h2) == 0.25

h3 = {}
assert RateLimitHeaderParser.parse_wait_seconds(h3) == 1.0
```

## Likely follow-ups

- Why should client wait times add a small randomized jitter to the parsed `Retry-After` header value?
- What maximum sleep cap should prevent an astronomical `Retry-After: 86400` from hanging worker threads?

---

[← Q0794](../../batch_08_azure_openai_bedrock_cloud_ai/0794_automated_error_categorizer_for_cloud_http_responses_in/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0796 →](../../batch_08_azure_openai_bedrock_cloud_ai/0796_load_shedding_under_extreme_cloud_ai_gateway_concurrency/README.md)

# Q0794 · Automated error categorizer for cloud HTTP responses in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Write Python code that inspects cloud AI HTTP response codes and error bodies, categorizing them as `RETRY_SAME`, `RETRY_ALTERNATE_PROVIDER`, or `FATAL`.

## Answer

```python
from typing import Any, Dict


class CloudAIErrorClassifier:
    @staticmethod
    def classify(status_code: int, error_body: str) -> str:
        if status_code == 429:
            # Quota exhausted -> retry alternate provider
            if "quota" in error_body.lower():
                return "RETRY_ALTERNATE_PROVIDER"
            return "RETRY_SAME"

        if status_code in {502, 503, 504}:
            return "RETRY_ALTERNATE_PROVIDER"

        if status_code == 400 and "context length" in error_body.lower():
            return "FATAL_PROMPT_TOO_LONG"

        if status_code in {400, 401, 403}:
            return "FATAL"

        return "UNKNOWN_FATAL"


assert CloudAIErrorClassifier.classify(429, "Rate limit reached") == "RETRY_SAME"
assert CloudAIErrorClassifier.classify(429, "Monthly token quota exceeded") == "RETRY_ALTERNATE_PROVIDER"
assert CloudAIErrorClassifier.classify(503, "Service Unavailable") == "RETRY_ALTERNATE_PROVIDER"
assert CloudAIErrorClassifier.classify(400, "Maximum context length is 8192") == "FATAL_PROMPT_TOO_LONG"
assert CloudAIErrorClassifier.classify(401, "Invalid API key") == "FATAL"
```

## Likely follow-ups

- How does the classifier extract retry delays from `Retry-After` headers?
- What metrics should be emitted when a `FATAL_PROMPT_TOO_LONG` error occurs?

---

[← Q0793](../../batch_08_azure_openai_bedrock_cloud_ai/0793_error_classification_transient_vs_terminal_cloud_ai_errors/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0795 →](../../batch_08_azure_openai_bedrock_cloud_ai/0795_rate_limit_header_parser_retry_after_x_ratelimit_reset/README.md)

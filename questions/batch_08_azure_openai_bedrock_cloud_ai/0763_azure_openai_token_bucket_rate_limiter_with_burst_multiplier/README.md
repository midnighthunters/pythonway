# Q0763 · Azure OpenAI token-bucket rate limiter with burst multiplier

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Write Python code implementing an enterprise token-bucket rate limiter that accommodates short-term burst multipliers while enforcing average TPM limits.

## Answer

Cloud providers allow short-term burst traffic above baseline quotas for a few seconds. A token-bucket algorithm models this with a burst capacity limit.

```python
import time


class BurstAwareTokenBucket:
    def __init__(self, tpm_limit: int, burst_multiplier: float = 1.5):
        self.tpm_limit = tpm_limit
        self.refill_per_second = tpm_limit / 60.0
        self.max_burst_capacity = tpm_limit * burst_multiplier
        self.tokens = float(tpm_limit)
        self.last_update = time.time()

    def consume(self, requested_tokens: int) -> bool:
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.max_burst_capacity, self.tokens + elapsed * self.refill_per_second)
        self.last_update = now

        if self.tokens >= requested_tokens:
            self.tokens -= requested_tokens
            return True
        return False


# 60,000 TPM = 1,000 tokens/sec refill; max burst = 90,000
bucket = BurstAwareTokenBucket(tpm_limit=60000, burst_multiplier=1.5)

# Consuming within normal baseline
assert bucket.consume(30000) is True
# Consuming remaining baseline
assert bucket.consume(30000) is True
# Exceeds available capacity
assert bucket.consume(1000) is False
```

## Likely follow-ups

- How does the burst multiplier prevent spurious 429 errors during multi-turn agent tool loops?
- How should tokens be replenished when handling asynchronous concurrent requests?

---

[← Q0762](../../batch_08_azure_openai_bedrock_cloud_ai/0762_azure_policy_enforcement_preventing_public_ip_creation_on/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0764 →](../../batch_08_azure_openai_bedrock_cloud_ai/0764_content_filtering_bypass_review_process_in_regulated_banks/README.md)

# Q0068 · Sustainable request rate from token quotas

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Capacity planning | Medium |

## Question

A deployment has a tokens-per-minute quota and a requests-per-minute quota. Some rate limiters count prompt tokens plus `max_tokens` toward the limit. Write a function for the sustainable request rate, and show the effect of an oversized `max_tokens`.

## Answer

Azure OpenAI, for example, estimates each request's token cost for rate limiting from the prompt plus `max_tokens`, so asking for far more output than you need burns quota.

```python
def sustainable_rpm(tpm_quota: int, rpm_quota: int, prompt_tokens: int, max_tokens: int) -> int:
    per_request = prompt_tokens + max_tokens
    if per_request <= 0:
        raise ValueError("token estimate must be positive")
    return min(rpm_quota, tpm_quota // per_request)


assert sustainable_rpm(300_000, 1_800, prompt_tokens=2_000, max_tokens=4_000) == 50
assert sustainable_rpm(300_000, 1_800, prompt_tokens=2_000, max_tokens=500) == 120
assert sustainable_rpm(10_000_000, 1_800, prompt_tokens=100, max_tokens=100) == 1_800
```

Right-sizing `max_tokens` here more than doubles throughput on the same quota.

Other levers: spread load across deployments and regions, provisioned throughput for steady traffic, prompt compression and caching, and client-side token-bucket limiting so you don't hammer the endpoint into 429s.

## Likely follow-ups

- How would you share one quota fairly between 30 client teams?

---

[← Q0067](../../batch_01_llm_fundamentals/0067_model_version_pinning_and_deprecation/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0069 →](../../batch_01_llm_fundamentals/0069_concurrency_planning_with_little_s_law/README.md)

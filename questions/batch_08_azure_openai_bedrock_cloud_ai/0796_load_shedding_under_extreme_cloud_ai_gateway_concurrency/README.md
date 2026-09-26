# Q0796 · Load shedding under extreme cloud AI gateway concurrency

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Explain the Load Shedding pattern. How does an AI gateway drop lower-priority requests gracefully during traffic surges to protect high-priority trading operations?

## Answer

When unexpected market events cause incoming traffic to exceed 300% of provisioned cloud AI capacity:
- Attempting to buffer all requests leads to memory exhaustion and catastrophic gateway crashes.
- All users experience cascading timeouts.

Load Shedding Architecture:
1. Priority Classification: Every request carries a priority tag (e.g. `Tier-1: Algorithmic Execution`, `Tier-2: Client Advisory Chat`, `Tier-3: Internal Employee Search`).
2. Queue Depth & Latency Thresholds:
   - If gateway P95 latency exceeds 2.5 seconds or queue depth exceeds 200 requests, load shedding engages.
3. Graceful Shedding (HTTP 503 with Retry-After):
   - Tier-3 requests are immediately rejected with a polite error: `"Service busy. High market volume; please retry in 30 seconds."`
   - Preserves 100% of compute capacity for Tier-1 trading execution without degradation.

## Likely follow-ups

- How does Little's Law ($L = \lambda W$) govern concurrency limits in load shedding?
- What are the differences between load shedding, rate limiting, and circuit breaking?

---

[← Q0795](../../batch_08_azure_openai_bedrock_cloud_ai/0795_rate_limit_header_parser_retry_after_x_ratelimit_reset/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0797 →](../../batch_08_azure_openai_bedrock_cloud_ai/0797_concurrency_limited_request_dispatcher_with_queue_reject_in/README.md)

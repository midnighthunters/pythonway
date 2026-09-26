# Q0793 · Error classification: transient vs terminal cloud AI errors

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

How does an AI gateway classify cloud HTTP error codes into transient (retryable) versus terminal (non-retryable) errors?

## Answer

Error Classification Taxonomies:

1. Transient / Retryable Errors:
   - `HTTP 429 Too Many Requests`: Rate limit or quota exhaustion; retry with exponential backoff or failover to secondary provider.
   - `HTTP 502 Bad Gateway` / `HTTP 503 Service Unavailable` / `HTTP 504 Gateway Timeout`: Cloud data center transient failure or load shedding; retry immediately on an alternate region.
   - `ConnectionResetError` / `TCP Read Timeout`: Network blips; safe to retry if idempotent.
2. Terminal / Non-Retryable Errors:
   - `HTTP 400 Bad Request`: Malformed JSON Schema, invalid parameter types, prompt context exceeds token window limit. Retrying will never succeed; fast-fail to caller.
   - `HTTP 401 Unauthorized` / `HTTP 403 Forbidden`: Expired credentials, invalid Entra ID permissions, or IP firewall violation. Fast-fail and alert security.
   - `Content Filter Triggered`: Prompt blocked by safety policy. Retrying identical prompt will always trigger the filter; return safety explanation.

## Likely follow-ups

- Under what circumstances can an HTTP 400 error actually be transient?
- How should the gateway communicate terminal errors to client UI frameworks?

---

[← Q0792](../../batch_08_azure_openai_bedrock_cloud_ai/0792_canary_traffic_splitter_for_model_a_b_testing_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0794 →](../../batch_08_azure_openai_bedrock_cloud_ai/0794_automated_error_categorizer_for_cloud_http_responses_in/README.md)

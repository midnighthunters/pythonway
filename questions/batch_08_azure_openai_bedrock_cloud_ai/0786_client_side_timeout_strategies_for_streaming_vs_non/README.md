# Q0786 · Client-side timeout strategies for streaming vs non-streaming calls

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Differentiate timeout strategies for streaming versus non-streaming LLM requests. Why does a single overall HTTP timeout fail for long agent responses?

## Answer

Timeout Failure Modes:
- Non-Streaming: An overall HTTP timeout (e.g. 30 seconds) works well. If the full response is not received in 30 seconds, abort.
- Streaming: A complex agent response generating 2,000 tokens may take 60 seconds total, but tokens stream steadily every 30 milliseconds. Applying a flat 30-second overall timeout kills healthy, active responses mid-sentence.

Dual-Timeout Strategy for Streaming:
1. Connect & TTFT Timeout:
   - Strict window (e.g. 5–10 seconds) from request dispatch until the first token arrives. If no tokens arrive, the provider is likely hanging or throttled; trip failover.
2. Inter-Token Read Timeout (Idle Timeout):
   - Strict window (e.g. 3–5 seconds) between consecutive streaming chunks.
   - As long as chunks keep arriving, the connection remains alive indefinitely regardless of total generation time.
   - If the stream stalls for more than 5 seconds, abort and report a network stall.

## Likely follow-ups

- How is the inter-token timeout configured in Python's `httpx` client?
- How does the client UI visually distinguish between an upstream timeout and an intentional pause in reasoning?

---

[← Q0785](../../batch_08_azure_openai_bedrock_cloud_ai/0785_streaming_sse_proxy_with_backpressure_handling/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0787 →](../../batch_08_azure_openai_bedrock_cloud_ai/0787_adaptive_timeout_manager_based_on_expected_token_count/README.md)

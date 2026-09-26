# Q0746 · Request deduplication for identical in-flight prompts

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

What is request coalescing (single-flight), and how does it prevent duplicate concurrent LLM queries from wasting cloud AI costs?

## Answer

In financial platforms, breaking news (e.g. a Federal Reserve interest rate announcement) triggers hundreds of internal analysts and trading bots to simultaneously submit identical queries ("Summarize Fed rate decision") within a 5-second window.

Single-Flight Coalescing:
- If Request 1 for prompt $X$ is currently in-flight to Azure OpenAI, the gateway detects that Request 2 arrives with an identical prompt hash before Request 1 has finished.
- Instead of launching a redundant second inference call, the gateway subscribes Request 2 to the in-flight future or stream of Request 1.
- When Request 1 finishes, the single generated completion is broadcast to both clients.
- Result: 50%–90% reduction in cloud token costs and GPU load during viral market news spikes.

## Likely follow-ups

- Why must single-flight coalescing check user security entitlements before sharing cached results?
- How does single-flight coalescing handle streaming chunk broadcasts?

---

[← Q0745](../../batch_08_azure_openai_bedrock_cloud_ai/0745_per_tenant_rate_limiting_with_sliding_window_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0747 →](../../batch_08_azure_openai_bedrock_cloud_ai/0747_implementing_an_in_flight_single_flight_request_coalescer/README.md)

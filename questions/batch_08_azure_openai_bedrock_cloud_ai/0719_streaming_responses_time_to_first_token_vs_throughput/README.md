# Q0719 · Streaming responses: Time To First Token vs Throughput

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Differentiate Time To First Token (TTFT) and throughput (tokens per second) in cloud LLM serving. How do gateways stream SSE chunks without blocking?

## Answer

Performance Metrics in Cloud LLM Serving:
1. Time To First Token (TTFT):
   - Duration from when the client sends the prompt until the first generated token arrives.
   - Dominated by prefill phase (processing the input prompt tokens and building the KV cache).
   - Critical for human perception of responsiveness in interactive chat applications (target: < 500ms).
2. Throughput / Generation Latency:
   - Rate at which subsequent tokens are generated (tokens per second per stream).
   - Dominated by decode phase (auto-regressive memory-bandwidth bound token generation).
   - Target: 30–80 tokens/sec for smooth conversational reading.

Gateway Streaming:
- Uses HTTP chunked transfer encoding (`Transfer-Encoding: chunked`) and `Content-Type: text/event-stream`.
- Gateways must disable internal output buffering (`X-Accel-Buffering: no` in Nginx) and flush chunks immediately as they arrive from Azure or Bedrock.

## Likely follow-ups

- Why does prompt length directly degrade TTFT while having minimal impact on generation token rate?
- How should connection drops mid-stream be handled by the client UI?

---

[← Q0718](../../batch_08_azure_openai_bedrock_cloud_ai/0718_weighted_round_robin_load_balancing_across_cloud_llm_regions/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0720 →](../../batch_08_azure_openai_bedrock_cloud_ai/0720_zero_data_retention_agreements_in_regulated_cloud_ai/README.md)

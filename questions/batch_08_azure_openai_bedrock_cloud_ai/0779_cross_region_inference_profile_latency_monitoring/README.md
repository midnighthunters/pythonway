# Q0779 · Cross-Region Inference profile latency monitoring

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

How do you measure latency variance and jitter introduced by dynamic cross-region routing in Amazon Bedrock?

## Answer

Measurement Methodology:
1. Client-Side Timing:
   - Measure $t_{start}$ (socket connection initiated), $t_{first\_token}$ (TTFT), and $t_{complete}$ (stream finished).
2. Regional Attribution:
   - Bedrock returns response headers indicating the actual physical serving region (e.g. `x-amzn-bedrock-invocation-region: us-east-2`).
3. Metrics & Dimensions:
   - Segment TTFT and P99 latency by serving region to detect inter-region fiber network congestion.
   - Jitter Calculation: Track standard deviation of TTFT across 1-minute rolling windows.

## Likely follow-ups

- What latency threshold should trigger pinning traffic to a local single-region endpoint?
- How does AWS Global Accelerator optimize inter-region packet routing?

---

[← Q0778](../../batch_08_azure_openai_bedrock_cloud_ai/0778_parsing_cloudtrail_bedrock_event_logs_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0780 →](../../batch_08_azure_openai_bedrock_cloud_ai/0780_measuring_cri_latency_variance_and_jitter_in_python/README.md)

# Q0748 · Health checks and canary deployments for LLM services

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

How do health checks and canary deployment strategies differ for non-deterministic LLM services compared to traditional REST microservices?

## Answer

Challenges with LLM Health Checks:
- Traditional microservices use simple `GET /healthz` returning `200 OK`.
- An LLM pod may have an alive HTTP server while its GPU memory is locked, its CUDA driver has crashed, or its model weights are corrupted, resulting in silent failures.

Synthetic Probing & Canary Strategy:
1. Deep Synthetic Probes:
   - Periodic readiness checks send a tiny prompt (e.g. `"ping"`, max tokens 1) to verify GPU Tensor Core computation, KV cache allocation, and token generation end-to-end.
2. Canary Rollouts with Statistical Verification:
   - When deploying a new model version or quantized checkpoint, 5% of traffic is routed to the canary pod.
   - Guardrail metrics track output schema validity, latency P99, and safety filter triggers against the stable baseline before promoting.

## Likely follow-ups

- Why should synthetic probe prompts use deterministic parameters (`temperature=0.0`)?
- How do you isolate synthetic probe tokens from billing chargeback metrics?

---

[← Q0747](../../batch_08_azure_openai_bedrock_cloud_ai/0747_implementing_an_in_flight_single_flight_request_coalescer/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0749 →](../../batch_08_azure_openai_bedrock_cloud_ai/0749_distributed_tracing_with_opentelemetry_genai_semantic/README.md)

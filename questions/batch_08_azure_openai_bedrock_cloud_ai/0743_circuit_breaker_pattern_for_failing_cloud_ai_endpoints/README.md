# Q0743 · Circuit breaker pattern for failing cloud AI endpoints

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Explain the Circuit Breaker pattern for cloud AI APIs. What are the three states, and how do they prevent cascade failures?

## Answer

When a cloud provider experiences an outage or severe latency degradation, client requests queue up, consuming memory, worker threads, and socket pools until the entire calling system crashes.

Circuit Breaker States:
1. Closed (Normal Operation):
   - All requests flow to the cloud provider. Failure counts are tracked within a rolling time window.
2. Open (Tripped / Broken):
   - If error rate exceeds a threshold (e.g. 5 consecutive 5xx or 429 errors), the breaker trips to Open.
   - For a configured duration (e.g. 30 seconds), all requests fail immediately or route instantly to a secondary provider without attempting network calls to the failing primary.
3. Half-Open (Testing Recovery):
   - After the timeout expires, a limited number of trial probe requests are sent to the primary endpoint.
   - If probes succeed, the breaker resets to Closed. If probes fail, it returns to Open.

## Likely follow-ups

- Why is an immediate failure in the Open state preferable to waiting for a 30-second network timeout?
- How does the circuit breaker pattern integrate with multi-cloud fallback routing?

---

[← Q0742](../../batch_08_azure_openai_bedrock_cloud_ai/0742_model_deprecation_and_graceful_version_migration_pipelines/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0744 →](../../batch_08_azure_openai_bedrock_cloud_ai/0744_implementing_a_stateful_circuit_breaker_in_python/README.md)

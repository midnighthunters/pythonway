# Q0742 · Model deprecation and graceful version migration pipelines

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Cloud AI providers routinely deprecate model versions (e.g. retiring older GPT-4 checkpoints). How does an enterprise gateway orchestrate seamless model migrations?

## Answer

Managing Model Deprecations in Regulated Environments:
1. Abstract Model Aliases:
   - Applications must never target vendor model checkpoint strings directly (e.g. `gpt-4-0613`).
   - Applications target logical aliases: `jpmc-model-standard`, `jpmc-model-reasoning`, `jpmc-model-fast`.
2. Gateway Shadowing (Dark Launch):
   - Before retiring Model A for Model B, the gateway duplicates production traffic, sending the secondary copy asynchronously to Model B.
   - Evaluation pipelines compare outputs, measuring regression in tool calling accuracy, JSON Schema adherence, and tone.
3. Traffic Shifting (Canary Rollout):
   - Weighted routing gradually shifts 5% -> 25% -> 50% -> 100% of live traffic to the new model version while monitoring error rates and latency.
4. Instant Rollback Capability:
   - If downstream trading algorithms experience formatting regressions, the alias is immediately repointed to the legacy model checkpoint.

## Likely follow-ups

- Why can a prompt that works reliably on GPT-4o fail on a newer point release?
- How do golden evaluation test sets gate automated model promotions?

---

[← Q0741](../../batch_08_azure_openai_bedrock_cloud_ai/0741_triton_inference_server_for_multi_model_serving/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0743 →](../../batch_08_azure_openai_bedrock_cloud_ai/0743_circuit_breaker_pattern_for_failing_cloud_ai_endpoints/README.md)

# Q0749 · Distributed tracing with OpenTelemetry GenAI semantic conventions

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

What are the OpenTelemetry GenAI semantic conventions, and what standardized span attributes must be recorded for LLM invocations?

## Answer

OpenTelemetry (OTel) defines vendor-neutral semantic conventions for GenAI systems to enable standardized observability across Jaeger, Datadog, Dynatrace, and Azure Application Insights.

Standard Span Attributes:
- `gen_ai.system`: Cloud or engine provider (e.g. `"azure_openai"`, `"aws.bedrock"`, `"vllm"`).
- `gen_ai.request.model`: Target model identifier (e.g. `"gpt-4o"`, `"claude-3-5-sonnet"`).
- `gen_ai.request.temperature` & `gen_ai.request.max_tokens`: Inference parameters.
- `gen_ai.usage.prompt_tokens`: Number of tokens in input prompt.
- `gen_ai.usage.completion_tokens`: Number of tokens in generated completion.
- `gen_ai.response.finish_reasons`: Stop reasons (`["stop"]`, `["tool_calls"]`, `["length"]`).

Security Note: Under banking compliance, prompt text and completion text are omitted from span attributes by default to prevent PII exposure in APM tools.

## Likely follow-ups

- How does `gen_ai.operation.name` distinguish between `"chat"`, `"text_completion"`, and `"embeddings"`?
- How do correlation headers link a frontend user click to downstream MCP tool spans?

---

[← Q0748](../../batch_08_azure_openai_bedrock_cloud_ai/0748_health_checks_and_canary_deployments_for_llm_services/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0750 →](../../batch_08_azure_openai_bedrock_cloud_ai/0750_building_an_opentelemetry_span_formatter_for_llm_invocations/README.md)

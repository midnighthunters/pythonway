# Q0360 · OpenTelemetry GenAI semantic conventions

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Observability | Medium |

## Question

What are the OpenTelemetry semantic conventions for generative AI, and why would a bank's platform adopt them?

## Answer

- OpenTelemetry defines standard attribute names for GenAI spans and metrics under the `gen_ai.*` namespace: for example the operation (chat, embeddings, tool execution), the provider, request model and response model, request parameters (temperature, max tokens), token usage (input and output tokens), response finish reasons, and agent and tool-call spans. Prompt and completion content is captured as opt-in events rather than default attributes, because of sensitivity.
- There are also standard metrics such as token usage and operation duration histograms.
- The conventions are still evolving (parts are marked experimental), so pin a version and check the current specification.

Why adopt them: vendor-neutral telemetry across Azure OpenAI, Bedrock and self-hosted models, one set of dashboards and alerts, easy export to the bank's existing observability stack, and compatibility with tools such as LangSmith and other OTel-aware backends. MCP's 2026-07-28 revision also documents trace-context propagation (`traceparent`) in request metadata, which lets traces cross MCP tool boundaries.

## Likely follow-ups

- Why is prompt content an opt-in event rather than a default span attribute?

---

[← Q0359](../../batch_04_llm_evaluation_observability/0359_traces_spans_and_attributes_for_llm_apps/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0361 →](../../batch_04_llm_evaluation_observability/0361_tracing_decorator_with_nested_spans/README.md)

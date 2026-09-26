# Q0359 · Traces, spans and attributes for LLM apps

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Observability | Easy |

## Question

What should a trace for one assistant request contain, and why are traces more useful than plain logs for LLM applications?

## Answer

A trace is a tree of spans for one request:
- Root span: request id, user and tenant (pseudonymised), assistant and version, total latency, status.
- Child spans: guardrail checks, query condensing, retrieval (query, filters, result ids and scores), reranking, each LLM call (model, parameters, prompt version, token usage, TTFT, finish reason), tool calls (name, arguments summary, result status, latency), and output validation.
- Events: retries, fallbacks, cache hits, guardrail triggers.

Why traces: LLM requests are multi-step and branching (agents loop, tools nest). A trace shows where time and tokens went, which step failed, and exactly what context the model saw. That is essential for debugging, evaluation (a trace becomes a test case), cost attribution and audit. Plain logs lose the causal structure.

Privacy: prompt and response content in traces is sensitive, so store it with access controls, redaction and retention rules, and keep metadata-only spans broadly visible.

## Likely follow-ups

- Which span attributes would you index for fast search?

---

[← Q0358](../../batch_04_llm_evaluation_observability/0358_detect_embedding_drift/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0360 →](../../batch_04_llm_evaluation_observability/0360_opentelemetry_genai_semantic_conventions/README.md)

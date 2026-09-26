# Q0366 · LangSmith for tracing and evaluation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Tooling | Medium |

## Question

How would you use LangSmith (or a similar LLM observability tool) in the development and production lifecycle of a LangGraph agent?

## Answer

- Tracing: set the environment variables or use the `@traceable` decorator, and LangChain and LangGraph runs are traced automatically: each node, LLM call, tool call, token usage and latency, plus the state at each step. It is useful for debugging agent loops and comparing runs.
- Datasets: turn interesting production traces (failures, edge cases) into dataset examples with reference outputs.
- Evaluation: run experiments over datasets with custom evaluators (code checks, LLM-as-judge, trajectory evaluators), compare prompts or models side by side, and track results over time. Wire this into CI.
- Prompt management: versioned prompts in a hub, pulled at runtime or at build time.
- Online evaluation and monitoring: automations that run evaluators on sampled production traces, feedback capture from the UI, and dashboards for latency, cost and error rates.
- Annotation queues for human review.

In a bank: check the deployment model (self-hosted or a regional data-residency option), what content is sent (redaction, masking of inputs and outputs), access controls and retention. Some teams export OpenTelemetry traces to their own stack instead, or as well.

## Likely follow-ups

- What data would you mask before sending traces to any observability vendor?

---

[← Q0365](../../batch_04_llm_evaluation_observability/0365_sample_traces_for_review/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0367 →](../../batch_04_llm_evaluation_observability/0367_dashboards_and_slos_for_genai_services/README.md)

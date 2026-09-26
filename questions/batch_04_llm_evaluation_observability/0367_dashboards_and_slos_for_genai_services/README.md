# Q0367 · Dashboards and SLOs for GenAI services

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Operations | Medium |

## Question

Define SLIs and SLOs for an internal GenAI chat service, and describe the dashboards you'd build.

## Answer

SLIs and example SLOs (monthly):
- Availability: successful responses divided by valid requests, at 99.9%.
- Time to first token: 95% of requests under 2 seconds. End-to-end latency: 95% under 12 seconds for standard answers.
- Quality proxy: the sampled groundedness pass rate at or above 95%, and citation validity at or above 98%.
- Safety: zero confirmed entitlement leaks (a hard objective, tracked by probes), and guardrail false-positive rate below an agreed level.
- Cost: cost per query within budget (tracked, not usually an SLO).

Dashboards:
1. A service-health overview: request rate, errors by type (provider 429s and 5xx, timeouts, validation failures), latency percentiles, TTFT, and error-budget burn.
2. A provider view: per-model and per-deployment latency, throttling, fallbacks and token throughput against quota.
3. A quality view: judge scores, abstention, feedback and citation validity, by assistant, version and language.
4. Cost: tokens and spend by tenant, model and assistant, and cache hit rates.
5. Safety and security: guardrail triggers, injection detections, leak-probe results.

Every panel is filterable by assistant, version and region, and linked to traces.

## Likely follow-ups

- Why is "quality" hard to express as an SLO, and what do you do instead?

---

[← Q0366](../../batch_04_llm_evaluation_observability/0366_langsmith_for_tracing_and_evaluation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0368 →](../../batch_04_llm_evaluation_observability/0368_slo_compliance_and_error_budget_for_ttft/README.md)

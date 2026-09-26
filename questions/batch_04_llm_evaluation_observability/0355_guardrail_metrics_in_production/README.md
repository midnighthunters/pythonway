# Q0355 · Guardrail metrics in production

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Online evaluation | Medium |

## Question

When you optimise an assistant for helpfulness, which "guardrail metrics" must not get worse, and how do you monitor them?

## Answer

Guardrail metrics are the ones you don't optimise for but must protect:
- Safety: policy-violation rate (sampled and judged), jailbreak or injection detection counts, PII leak detections in outputs.
- Security: entitlement-leak test results (synthetic probes run continuously), blocked tool calls.
- Faithfulness: sampled groundedness scores and citation validity rate.
- Abstention and refusal: over-refusal and under-abstention on monitored samples.
- Operational: p95 latency and TTFT, error rate, cost per query, token usage per turn.
- User trust: negative feedback rate, escalations to humans.

Monitor them per release and variant, with alert thresholds. Any A/B test or rollout decision must show "no significant degradation" on guardrails, not just a win on the primary metric.

## Likely follow-ups

- Which guardrail metric would make you roll back even if helpfulness improved?

---

[← Q0354](../../batch_04_llm_evaluation_observability/0354_a_b_test_an_assistant_change/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0356 →](../../batch_04_llm_evaluation_observability/0356_implicit_feedback_signals/README.md)

# B0095 · Production-ready for an agentic capability

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Engineering practice | Hard |

## Question

What is your definition of "production-ready" for an agentic capability?

## Answer

- Quality: an evaluation suite (task success, tool-call accuracy, safety) that meets agreed thresholds, with regression tests in CI.
- Safety and security: least-privilege tools, user-delegated auth, approval before side effects, prompt-injection mitigations, output validation, red-team findings addressed, data classification approved.
- Reliability: timeouts, retries, idempotency, step and cost limits, durable state (checkpointing), graceful degradation, load testing.
- Observability: traces of every step and tool call; metrics for latency, cost, errors and safety flags; dashboards, alerts and audit logs.
- Operations: runbooks, named on-call owners, a kill switch, rollback for prompts, models and code.
- Governance: documentation, model-risk sign-off where required, user guidance.

## Likely follow-ups

- Which of these do teams skip most often?
- How do you test an agent's behaviour under failure?

---

[← B0094](../../behavioural_questions/0094_your_approach_to_code_reviews/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0096 →](../../behavioural_questions/0096_how_you_document_your_work/README.md)

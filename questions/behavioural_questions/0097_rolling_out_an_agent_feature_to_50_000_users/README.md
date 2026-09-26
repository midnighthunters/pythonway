# B0097 · Rolling out an agent feature to 50,000 users

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Scenario | Hard |

## Question

How would you roll out a new agent feature to 50,000 employees safely?

## Answer

- Readiness: evaluations pass, load tests at the expected concurrency (streams and tool calls), quota or provisioned capacity reserved, security sign-off.
- Staged rollout: dogfood → 1% → 10% → 50% → 100%, each step gated on error rate, latency, cost, safety flags and feedback, with flags per cohort or business unit.
- Guardrails: per-user rate limits, cost caps, a kill switch, fallback to the non-agent path.
- Monitoring: per-cohort dashboards, alert thresholds, on-call cover during rollout windows.
- Communication: release notes, training material, known limitations, a feedback channel, a briefed support team.
- After launch: review the metrics, triage feedback, iterate.

## Likely follow-ups

- Which metric would make you halt the rollout?
- How do you handle a usage spike on launch day?

---

[← B0096](../../behavioural_questions/0096_how_you_document_your_work/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0098 →](../../behavioural_questions/0098_on_call_and_sustainable_pace/README.md)

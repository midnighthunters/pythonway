# B0088 · Onboarding a new model to the platform

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Scenario | Medium |

## Question

A new frontier model has just launched. How would you add it to a model-agnostic platform?

## Answer

- Approval: vendor and legal terms, data handling, regional availability, model-risk intake.
- Technical: adapter support (API shape, tool calling, structured output, streaming events, token accounting, error codes) and a capability-registry entry (context window, modalities, reasoning controls, price).
- Evaluation: the platform suites (task quality, safety and jailbreak resistance, format adherence, latency, cost) compared with the incumbent models, plus per-model prompt tuning.
- Capacity: quotas or provisioned throughput, rate limits, regional deployments, fallback mapping.
- Rollout: internal dogfooding → opt-in beta → default for specific routes, with monitoring, docs and release notes.

## Likely follow-ups

- Which evaluation results would block the rollout?
- How do you avoid prompt regressions across models?

---

[← B0087](../../behavioural_questions/0087_prototype_demo_wanted_in_production_in_two_weeks/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0089 →](../../behavioural_questions/0089_primary_model_endpoint_failing/README.md)

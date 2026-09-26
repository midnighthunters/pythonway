# Q0394 · Ongoing monitoring for model risk management

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Governance | Medium |

## Question

After model-risk approval, what ongoing monitoring does a GenAI assistant need to stay compliant?

## Answer

- Performance monitoring against the validated baseline: sampled quality and groundedness scores, abstention and refusal rates, by segment, with thresholds that trigger review.
- Drift: query-distribution and topic drift, corpus changes, and provider model version changes (which are a change to the model itself).
- Stability of controls: guardrail effectiveness, entitlement-leak probes, PII detections, incident counts.
- Usage within approved scope: the assistant is used for the approved purpose and population (detect scope creep, such as people using a drafting tool for decisions).
- Periodic revalidation: scheduled (for example annual) or triggered (major model upgrade, new data sources, new use cases, an incident).
- Documentation and evidence: the monitoring reports are archived, issues are tracked to resolution, and model inventory entries stay current.
- Clear ownership: a model owner, a monitoring owner and escalation paths.

Automate the evidence collection from the evaluation and observability platform, so compliance doesn't depend on manual spreadsheets.

## Likely follow-ups

- Which events should automatically trigger revalidation?

---

[← Q0393](../../batch_04_llm_evaluation_observability/0393_turn_red_team_findings_into_regression_tests/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0395 →](../../batch_04_llm_evaluation_observability/0395_total_cost_including_human_rework/README.md)

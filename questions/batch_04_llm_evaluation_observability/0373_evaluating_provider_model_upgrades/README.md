# Q0373 · Evaluating provider model upgrades

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Release engineering | Medium |

## Question

A provider announces that a model version you use will be retired in 90 days, and you must move to its successor. What's your plan?

## Answer

1. Inventory: which assistants, prompts and deployments use the old version (from the model registry and telemetry).
2. Offline evaluation: run the full golden sets and safety suites on the new version with the current prompts. Compare quality, format adherence, tool-calling behaviour, refusal rates, latency, token usage (the new model may be more verbose) and cost.
3. Fix regressions: adjust prompts, create per-model variants, or change parameters. Re-run the evaluations.
4. Validation: update the model-risk documentation, re-run the red team, and get sign-off from the owners.
5. Rollout: shadow, then canary, then gradual ramp, with dashboards per version and a rollback option while the old version still exists.
6. Clean-up: remove old configurations, and update pinned versions in code and infrastructure.

Start early. Deprecation windows can be short, and a platform with many assistants needs automation for this, not heroics.

## Likely follow-ups

- What would you do if the successor regresses on one critical assistant?

---

[← Q0372](../../batch_04_llm_evaluation_observability/0372_shadow_testing_a_new_model/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0374 →](../../batch_04_llm_evaluation_observability/0374_maintaining_the_golden_set/README.md)

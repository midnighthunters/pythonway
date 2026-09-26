# Q0372 · Shadow testing a new model

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Release engineering | Medium |

## Question

What is shadow testing for LLM changes, and what are its benefits and pitfalls?

## Answer

- Shadow testing mirrors a sample of real production requests to the new configuration (a model, prompt or retriever) without showing its outputs to users. You then compare the outputs offline: judge scores, pairwise preferences against production, format validity, latency and cost.
- Benefits: real traffic distribution with zero user risk, and early detection of regressions and edge cases that the golden set misses.
- Pitfalls:
  - Cost (you pay for double inference), so sample.
  - Side effects: the shadow must never execute real tool actions (sending email, moving money). Stub the tools or run them read-only.
  - Privacy: the mirrored data must stay within the same controls and entitlements.
  - Rate limits: the shadow traffic mustn't eat production quota.
  - Multi-turn divergence: the shadow sees production's history, not its own, so it tests single turns best.

## Likely follow-ups

- How would you shadow-test an agent that normally calls write tools?

---

[← Q0371](../../batch_04_llm_evaluation_observability/0371_canary_analysis_for_prompt_or_model_rollouts/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0373 →](../../batch_04_llm_evaluation_observability/0373_evaluating_provider_model_upgrades/README.md)

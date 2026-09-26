# Q0388 · Reporting evaluation results to stakeholders

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Communication | Easy |

## Question

How do you present evaluation results to business owners and risk partners so they can make a launch decision?

## Answer

- Lead with the decision and the criteria: "We recommend launching to the Finance pilot. It meets 5 of 6 agreed criteria. The exception is French-language accuracy (78% against a target of 85%), which is mitigated by English-only rollout."
- A scorecard against the pre-agreed targets: quality, safety, abstention, latency, cost, with confidence intervals or sample sizes.
- Slices that matter to them: business lines, languages, question types.
- Concrete examples: 3–5 good answers and 3–5 failures with explanations. These build intuition far better than numbers.
- Known limitations and mitigations: what users should verify, human review steps, and monitoring.
- What changed since last time, and the plan for the next iteration.
- Methodology in an appendix: dataset, judges and their calibration, the run manifest.

Avoid jargon (nDCG, kappa) in the headline, and never present a single number without its uncertainty and context.

## Likely follow-ups

- How do you present a result that is "good on average but bad for one group"?

---

[← Q0387](../../batch_04_llm_evaluation_observability/0387_evaluation_run_manifest/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0389 →](../../batch_04_llm_evaluation_observability/0389_fairness_evaluation_across_groups/README.md)

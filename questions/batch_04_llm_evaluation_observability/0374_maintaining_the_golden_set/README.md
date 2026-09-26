# Q0374 · Maintaining the golden set

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Datasets | Medium |

## Question

Six months after launch, your golden set gives great scores but users complain. What went wrong, and how do you maintain the set?

## Answer

Likely causes: the set no longer matches production (drift), documents changed so expected answers are stale, prompts were tuned against the set (over-fitting), and it lacks the hard or new cases users now bring.

Maintenance practices:
- Refresh from production regularly (weekly or monthly): sample new queries by cluster and intent, prioritise failures (negative feedback, escalations, judge fails), and label them.
- Keep a frozen held-out subset that is never used for tuning, only for reporting.
- Re-validate labels when source documents change (link cases to document versions).
- Retire obsolete cases, and track the set's composition over time (slice counts).
- Version it (dataset hash in reports), with changelogs and owners.
- Periodically audit a sample with SMEs, and compare offline scores with online metrics to check they still correlate.

## Likely follow-ups

- Why keep a frozen held-out subset if you're adding new cases anyway?

---

[← Q0373](../../batch_04_llm_evaluation_observability/0373_evaluating_provider_model_upgrades/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0375 →](../../batch_04_llm_evaluation_observability/0375_check_for_evaluation_leakage/README.md)

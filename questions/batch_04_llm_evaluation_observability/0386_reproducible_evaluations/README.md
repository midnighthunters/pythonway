# Q0386 · Reproducible evaluations

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation integrity | Medium |

## Question

Two engineers run "the same" evaluation and get different numbers. What must be pinned or recorded to make evaluations reproducible?

## Answer

- Data: the evaluation dataset version (hash), the corpus and index version for RAG, and document snapshots.
- System: the code commit, prompt versions, model identifiers and deployment versions (never floating aliases), sampling parameters, tool implementations and their fixtures, and guardrail configurations.
- Evaluators: the judge model and version, judge prompt versions, metric code versions and thresholds.
- Randomness: seeds for sampling cases and shuffling. The number of repeated runs, and how results are aggregated (mean, pass^k).
- Environment: dependency versions, date and time injected into prompts (a fixed "today"), region.
- Outputs: store raw outputs and per-case scores, not just aggregates, so results can be re-scored and audited.

Accept that hosted models aren't bit-for-bit deterministic. Report variance across repeated runs, and compare distributions rather than single numbers.

## Likely follow-ups

- Why store raw outputs rather than only scores?

---

[← Q0385](../../batch_04_llm_evaluation_observability/0385_rate_limit_evaluation_traffic_with_a_token_bucket/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0387 →](../../batch_04_llm_evaluation_observability/0387_evaluation_run_manifest/README.md)

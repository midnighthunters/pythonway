# Q0302 · The evaluation pyramid for GenAI

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation strategy | Medium |

## Question

Describe a layered evaluation strategy for an LLM application, from cheapest to most expensive.

## Answer

1. Deterministic unit tests (every commit, seconds): prompt rendering, parsers, schema validation, tool dispatch, guardrail regexes, and fake-LLM tests of control flow.
2. Deterministic output checks on real model runs: schema validity, citation format, required sections, length, forbidden content, numbers present in the sources.
3. Reference-based metrics on a golden set: exact or field match for extraction and classification, retrieval hit rate, key-point coverage.
4. Model-graded metrics: LLM-as-judge for faithfulness, relevance and rubric quality, calibrated against human labels.
5. Human evaluation: expert review of samples, side-by-side comparisons for major changes, and red-teaming.
6. Online evaluation: A/B tests, canaries, user feedback, implicit signals, and sampled production traces scored by judges.

Gate merges on layers 1–3 (fast and cheap), releases on layers 3–5 thresholds, and use 6 to catch what offline evaluation misses. Feed production failures back into layer 3.

## Likely follow-ups

- Which layers belong in the pull-request pipeline, and which in a nightly job?

---

[← Q0301](../../batch_04_llm_evaluation_observability/0301_why_llm_evaluation_is_hard/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0303 →](../../batch_04_llm_evaluation_observability/0303_define_success_criteria_before_building/README.md)

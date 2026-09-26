# Q0383 · Error analysis workflow

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Error analysis | Medium |

## Question

Describe a practical error-analysis workflow for improving an LLM application.

## Answer

1. Collect failures: evaluation fails, negative feedback, judge fails on sampled production traces, and escalations. Include the full trace (input, retrieved context, prompt version, output).
2. Read them. Open coding first: write free-text notes on 50–100 failures without predefined categories.
3. Build a taxonomy from the notes (axial coding): 5–10 categories with definitions (retrieval miss, stale source, wrong number, ignored instruction, bad clarification, tool-argument error, and so on).
4. Label the rest with the taxonomy, possibly with LLM assistance validated by humans.
5. Prioritise by frequency × severity × fixability.
6. Fix the top bucket with a targeted change (data, retrieval, prompt, tool design, guardrail), and add the failures as regression cases.
7. Re-evaluate the whole set, checking for side effects, and repeat.

This loop, with humans reading real outputs, usually beats metric-watching alone. Many teams skip step 2, and that's where the insight comes from.

## Likely follow-ups

- Why read raw failures before defining categories?

---

[← Q0382](../../batch_04_llm_evaluation_observability/0382_error_taxonomy_counts/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0384 →](../../batch_04_llm_evaluation_observability/0384_load_test_an_llm_endpoint/README.md)

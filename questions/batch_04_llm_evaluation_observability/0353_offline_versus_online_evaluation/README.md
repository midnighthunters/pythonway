# Q0353 · Offline versus online evaluation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation strategy | Easy |

## Question

Compare offline and online evaluation for LLM applications. Why do you need both?

## Answer

- Offline: fixed datasets, run before release. It is controlled, repeatable and safe (no user exposure), and good for gating changes and comparing versions. Its limits: dataset coverage, staleness, and proxy metrics that may not match user value.
- Online: real traffic after (or during) release, through A/B tests, canaries, feedback, implicit signals and sampled judge scoring. It captures the real distribution and real outcomes. Its limits: noisy signals, slower, users are exposed to regressions, and privacy constraints on reviewing content.

You need both. Offline evaluation prevents shipping known regressions, and online evaluation reveals what offline missed. Close the loop by turning online failures into offline cases, and checking that offline metrics predict online outcomes.

## Likely follow-ups

- How would you check that your offline metric actually predicts user satisfaction?

---

[← Q0352](../../batch_04_llm_evaluation_observability/0352_annotation_guidelines_and_quality_control/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0354 →](../../batch_04_llm_evaluation_observability/0354_a_b_test_an_assistant_change/README.md)

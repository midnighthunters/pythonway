# Q0091 · Benchmark contamination

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Evaluation integrity | Medium |

## Question

What is benchmark contamination, and why should you be sceptical of public leaderboard scores when choosing a model?

## Answer

- Contamination means test items, or close paraphrases of them, appeared in the model's training data, so the score measures memorisation rather than capability. Public benchmarks are all over the web and easily leak.
- Other distortions: tuning to a specific benchmark format, selective reporting, prompt or harness differences, and saturated benchmarks where top models differ only by noise.
- Detection hints: near-verbatim completion of test items, a big gap between the public score and a fresh held-out set, and perplexity anomalies.

For your decisions: treat leaderboards as a shortlist filter only. Evaluate on private, task-specific sets built from your own (approved) data, refresh them periodically, and keep them out of anything that might be used for training or shared publicly.

## Likely follow-ups

- How would you protect your internal evaluation set from leaking into vendor training data?

---

[← Q0090](../../batch_01_llm_fundamentals/0090_model_documentation_for_model_risk_management/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0092 →](../../batch_01_llm_fundamentals/0092_vocabulary_size_trade_offs/README.md)

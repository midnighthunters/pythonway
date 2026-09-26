# Q0303 · Define success criteria before building

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation strategy | Easy |

## Question

A business team asks for "an AI assistant for Treasury operations". What evaluation criteria would you agree on before building?

## Answer

- Task definition: which questions or tasks are in scope (with examples), and which are explicitly out of scope.
- Quality metrics with targets: for example 90% of answers rated correct and complete by Treasury SMEs, 98% of cited sources actually supporting the claim, and 95% abstention on unanswerable questions.
- Safety and compliance: zero entitlement leaks in the leak test suite, PII policy adherence, refusal of out-of-scope advice.
- Operational: p95 time to first token under 2 seconds, availability 99.9%, cost per query under an agreed amount.
- Business outcome: time saved per task compared with a measured baseline, and adoption.
- Evaluation method: who labels (SMEs), how many cases, how often it is refreshed, and who signs off.

Writing these down first prevents endless "is it good enough?" debates and gives model-risk reviewers the evidence they need.

## Likely follow-ups

- How would you set a realistic accuracy target before you have a prototype?

---

[← Q0302](../../batch_04_llm_evaluation_observability/0302_the_evaluation_pyramid_for_genai/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0304 →](../../batch_04_llm_evaluation_observability/0304_evaluation_dataset_schema/README.md)

# Q0301 · Why LLM evaluation is hard

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation foundations | Easy |

## Question

Why is evaluating LLM applications harder than testing traditional software?

## Answer

- Many correct answers: free text can be right in many phrasings, so exact-match assertions don't work for most outputs.
- Non-determinism: the same input can give different outputs across runs, model versions and even batch composition.
- Silent regressions: a prompt tweak or provider model update can improve one case type and break another with no error thrown.
- Compound systems: retrieval, prompts, tools, guardrails and models interact, so failures need attributing to a stage.
- Subjective and contextual quality: helpfulness, tone and "good enough" depend on the user and task. Some qualities (faithfulness, safety) need expert judgement.
- Distribution shift: production questions differ from your test set and drift over time.
- Cost: running evaluations (especially LLM judges and human review) costs money and time.

Consequence: you need layered evaluation (deterministic checks, model-graded metrics, human review, online monitoring), versioned datasets, repeated runs, and statistical care when comparing versions.

## Likely follow-ups

- Which of these problems also exist for traditional ML models?

---

[← Q0300](../../batch_03_rag_retrieval/0300_design_entitlement_aware_enterprise_rag_for_llm_suite/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0302 →](../../batch_04_llm_evaluation_observability/0302_the_evaluation_pyramid_for_genai/README.md)

# Q0308 · Why BLEU and ROUGE mislead for LLM outputs

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Metrics | Medium |

## Question

A vendor reports a high BLEU score for their summarisation model. Why should you be sceptical?

## Answer

- BLEU and ROUGE measure n-gram overlap with one or a few references. LLM outputs legitimately use different wording, so good answers get low scores and fluent wrong answers can score well.
- They are insensitive to meaning-critical details: negation, numbers, entity swaps ("approved" and "not approved" share most n-grams).
- They reward length and copying behaviours depending on the variant.
- Scores aren't comparable across datasets, tokenisation or reference sets, and they saturate with strong models.

What to ask for instead: task-specific evaluation on your own data, faithfulness and factual-consistency scores, key-point coverage, human preference or rubric ratings, and error analysis with examples. Overlap metrics can stay as cheap regression signals.

## Likely follow-ups

- In which task are BLEU-style metrics still reasonable?

---

[← Q0307](../../batch_04_llm_evaluation_observability/0307_rouge_l_with_longest_common_subsequence/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0309 →](../../batch_04_llm_evaluation_observability/0309_semantic_similarity_scoring_and_its_limits/README.md)

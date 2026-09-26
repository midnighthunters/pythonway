# B0063 · Making a significant performance improvement

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - performance | Medium |

## Question

Tell me about a time you made a significant performance improvement.

## Answer

- Measure first: profile (py-spy, tracing spans) instead of guessing.
- Example: chat p95 was 12 seconds. Traces showed sequential retrieval, reranking and two LLM calls. You parallelised retrieval, cached embeddings, streamed the answer, moved one call to a smaller model and trimmed prompts by 40%.
- Result: time to first token 4s → 0.9s, p95 end-to-end 12s → 6s, cost down 30%.
- Mention that you ran the evaluation suite to confirm quality did not regress.

## Likely follow-ups

- How did you make sure quality didn't drop?
- What did you try that didn't help?

---

[← B0062](../../behavioural_questions/0062_improving_reliability_of_a_system/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0064 →](../../behavioural_questions/0064_turning_ambiguity_into_a_concrete_plan/README.md)

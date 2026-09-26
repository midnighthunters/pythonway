# Q0027 · Why LLMs hallucinate

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Reliability | Medium |

## Question

Why do LLMs hallucinate, and which engineering levers actually reduce it in a production assistant?

## Answer

Why it happens:
- The training objective rewards plausible continuations, not truth. The model has no built-in "I don't know" signal unless it has been trained to produce one.
- Knowledge is compressed and lossy. Rare facts such as internal policy numbers are poorly memorised, and knowledge has a cutoff date.
- Evaluation and RLHF pressure can reward confident answers over abstaining.
- The context may be missing, contradictory, or buried in a very long prompt ("lost in the middle").

Levers that work:
- Grounding: RAG with entitlement-aware retrieval, plus an instruction to answer only from the provided sources, with citations.
- Allow and reward abstention ("If the documents don't contain the answer, say so").
- Tools for facts and calculation (search, SQL, calculators) instead of parametric memory.
- Structured output with validation, and verification steps (citation checking, a second-pass faithfulness judge).
- Lower temperature for factual tasks, and use a stronger model for high-stakes routes.
- Measure it with groundedness and faithfulness evaluations on a golden set, and monitor it online.
- UX: show sources, and make it easy for users to verify.

## Likely follow-ups

- How would you measure the hallucination rate of a policy Q&A assistant?
- Can RAG itself cause hallucinations? (Irrelevant or conflicting chunks.)

---

[← Q0026](../../batch_01_llm_fundamentals/0026_next_token_cross_entropy_loss/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0028 →](../../batch_01_llm_fundamentals/0028_context_window_limits_and_lost_in_the_middle/README.md)

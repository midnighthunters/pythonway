# Q0245 · Build a retrieval golden set

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Retrieval evaluation | Medium |

## Question

How do you build a labelled evaluation set for an enterprise RAG system, and keep it useful over time?

## Answer

1. Source real questions: search logs, helpdesk tickets and pilot-user sessions, with approval and de-identification, plus interviews with domain owners about critical questions.
2. Cover the distribution: common questions, long-tail questions, identifier lookups, multi-hop questions, time-sensitive questions ("current policy"), unanswerable questions, and questions that must be refused for entitlement reasons, per user persona.
3. Label: for each question, the relevant chunk or document ids (graded if possible), the reference answer or key facts, and the expected behaviour (answer or abstain). Have domain experts review, and measure inter-annotator agreement on a subset.
4. Size: start with 100–300 questions for development, plus a held-out set. Grow it with production failures.
5. Maintain it: version the set alongside the corpus. Documents change, so labels go stale. Re-validate labels when source documents update, and retire obsolete questions.
6. Protect it: keep it out of prompts and few-shot examples, and away from anything used for vendor training.

## Likely follow-ups

- How do you keep labels valid when the policy documents are revised?

---

[← Q0244](../../batch_03_rag_retrieval/0244_ndcg_for_graded_relevance/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0246 →](../../batch_03_rag_retrieval/0246_synthetic_questions_for_retrieval_evaluation/README.md)

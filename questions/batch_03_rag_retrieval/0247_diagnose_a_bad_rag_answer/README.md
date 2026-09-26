# Q0247 · Diagnose a bad RAG answer

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Debugging | Medium |

## Question

A user says the assistant gave a wrong answer about the parental leave policy. How do you find out whether it is a retrieval, context or generation problem?

## Answer

Work through the trace (retrieval ids, scores, prompt, model output):
1. Was the right document in the index at all? Check ingestion (parsing failed, stale version, wrong ACL, deleted).
2. Was it retrieved? Look at its rank in the BM25, vector and fused lists. If missing, it's a query problem (rewrite, filters, acronyms) or an embedding or chunking problem.
3. Did it survive reranking and packing? It may have been cut by the budget, the per-document cap or a threshold.
4. Did the prompt contain the right chunk, but in the middle of a long context, or alongside a conflicting old version?
5. Did the model misuse good context? Check faithfulness (wrong number, ignored qualifier, merged two policies). That's a generation problem: prompt, model or temperature.
6. Was the answer right but the question misread? For example UK versus US policy: missing jurisdiction context.

Then add the case to the evaluation set, fix the failing stage, and check for regressions across the set.

## Likely follow-ups

- Which telemetry must you capture per request to make this diagnosis possible?

---

[← Q0246](../../batch_03_rag_retrieval/0246_synthetic_questions_for_retrieval_evaluation/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0248 →](../../batch_03_rag_retrieval/0248_recency_boosting_with_time_decay/README.md)

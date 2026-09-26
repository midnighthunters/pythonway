# Q0298 · RAG failure-mode checklist

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Debugging | Medium |

## Question

List the common RAG failure modes by pipeline stage, as you'd use them in a design review or post-incident analysis.

## Answer

- Ingestion: parser dropped tables or text, stale or missing documents, duplicate copies, wrong or missing ACLs, boilerplate noise, bad OCR.
- Chunking: answers split across boundaries, chunks without context, oversized chunks diluting embeddings.
- Indexing: mixed embedding model versions, filterable fields not indexed, deletions not propagated.
- Query understanding: follow-ups not condensed, acronyms and jargon mismatch, identifiers searched semantically, wrong inferred filters.
- Retrieval: poor recall (dense-only), post-filtering starvation, entitlement leaks, recency or authority not considered.
- Reranking and packing: good chunks cut by the budget, duplicates crowding out diversity, lost-in-the-middle ordering.
- Generation: unfaithful answers (numbers, negation), not abstaining, citation errors, ignoring conflicts between versions, prompt injection from content.
- Post-processing and UX: unsanitised markdown, citations not linked, streaming leaks before checks.
- Operations: ACL sync lag, index freshness lag, provider throttling, no evaluation gate on changes.

## Likely follow-ups

- Which three would you test for automatically in CI?

---

[← Q0297](../../batch_03_rag_retrieval/0297_end_to_end_mini_rag_pipeline/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0299 →](../../batch_03_rag_retrieval/0299_cost_model_for_a_rag_service/README.md)

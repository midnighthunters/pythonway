# Q0286 · Hierarchical summaries as retrieval units

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Advanced retrieval | Medium |

## Question

Some questions are about a whole document or corpus ("what are the main themes of this year's audit findings?"). How do hierarchical summary indexes (for example RAPTOR-style trees) help?

## Answer

- Build a tree: chunk-level leaves, then cluster related chunks and write summaries of each cluster, then summarise the summaries, up to document or corpus level.
- Index every level. Specific questions match leaves, and broad questions match higher-level summaries, which capture themes that no single chunk contains.
- At query time, retrieve across levels (or traverse top-down), and cite the leaves underneath each summary for verifiability.

Trade-offs: an extra LLM cost at ingestion, summaries go stale when documents change (rebuild affected branches), and summaries can introduce errors, so keep links to the underlying sources. For "global" questions over a large corpus, this (or a GraphRAG community-summary approach) beats plain top-k chunk retrieval.

## Likely follow-ups

- How would you keep the summary tree fresh as documents change daily?

---

[← Q0285](../../batch_03_rag_retrieval/0285_scan_documents_for_injection_patterns_at_ingestion/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0287 →](../../batch_03_rag_retrieval/0287_index_generated_question_answer_pairs/README.md)

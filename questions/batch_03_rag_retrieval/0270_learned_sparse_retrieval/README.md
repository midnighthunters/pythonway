# Q0270 · Learned sparse retrieval

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Advanced retrieval | Medium |

## Question

What are learned sparse retrievers such as SPLADE, and where do they fit between BM25 and dense embeddings?

## Answer

- A transformer maps text to a sparse, vocabulary-sized vector of term weights. Unlike BM25, it learns term importance and expansion: a document about "reimbursement" can get weight on "expenses" and "refund" even if those words never appear.
- It is stored and queried in an inverted index (like BM25), so it gets the efficiency and exact-term behaviour of lexical search plus some semantic generalisation.
- Quality is often competitive with dense retrieval, and the combination (sparse plus dense) is strong.
- Trade-offs: an encoding model at both index time and query time, a larger index than BM25, domain adaptation needs, and support that varies by search engine (OpenSearch has neural sparse search, and Elasticsearch has ELSER).

It is a good option when identifier and term precision matter (typical in enterprise search) but plain BM25 misses paraphrases.

## Likely follow-ups

- Why can learned sparse vectors be easier to debug than dense ones?

---

[← Q0269](../../batch_03_rag_retrieval/0269_late_interaction_maxsim_scoring/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0271 →](../../batch_03_rag_retrieval/0271_synonym_expansion_for_enterprise_queries/README.md)

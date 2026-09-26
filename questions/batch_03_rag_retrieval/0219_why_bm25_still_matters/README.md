# Q0219 · Why BM25 still matters

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Hybrid search | Easy |

## Question

If we have good embeddings, why keep a keyword (BM25) index in an enterprise RAG system?

## Answer

- Exact identifiers: policy numbers ("POL-4471"), product codes, error codes, ticker symbols, names and acronyms. Embeddings often blur these, and BM25 nails them.
- Rare domain terms and new jargon the embedding model never saw.
- Negation and precise wording sometimes favour lexical matching.
- Explainability: you can say which terms matched, which is useful for debugging and user trust.
- Zero training, cheap, and fast, with mature filtering and access-control features in search engines.
- Robustness: when embeddings fail on a query type, hybrid search degrades gracefully.

Hybrid search (BM25 plus vectors, fused with RRF or weighted scores) consistently beats either alone on mixed enterprise query sets. Measure it on your own labelled queries.

## Likely follow-ups

- Which query types in a bank would you expect BM25 to win?

---

[← Q0218](../../batch_03_rag_retrieval/0218_bm25_scoring_from_scratch/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0220 →](../../batch_03_rag_retrieval/0220_vector_search_with_metadata_filters/README.md)

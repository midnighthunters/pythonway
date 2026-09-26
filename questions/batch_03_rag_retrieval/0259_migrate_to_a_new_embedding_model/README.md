# Q0259 · Migrate to a new embedding model

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Operations | Medium |

## Question

You want to switch to a better embedding model for 50M chunks. How do you migrate without downtime or a quality regression?

## Answer

1. Evaluate offline: compare recall@k and nDCG on the golden set, with the old and new models, both in hybrid mode with the reranker, by query type and language.
2. Build a new index side by side (blue-green): re-embed in the background with rate limiting and checkpoints, and track progress. Vectors from different models can't be mixed in one index.
3. Dual-write new and changed documents to both indexes during the backfill.
4. Shadow: send a sample of live queries to the new index, and compare overlap and judge scores without affecting users.
5. Canary: route a small share of traffic, and watch answer quality, feedback, latency and cost.
6. Cut over with a feature flag, keep the old index for fast rollback, then decommission it.
7. Update the metadata (the `embedding_model` field) and cached embeddings and query embeddings, and any semantic caches (their similarity thresholds change).

Budget the re-embedding cost and quota, and schedule it off-peak.

## Likely follow-ups

- Why must semantic-cache thresholds be re-fitted after the switch?

---

[← Q0258](../../batch_03_rag_retrieval/0258_cache_embeddings_by_content_and_model/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0260 →](../../batch_03_rag_retrieval/0260_choosing_a_vector_store/README.md)

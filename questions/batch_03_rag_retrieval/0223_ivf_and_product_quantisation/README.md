# Q0223 · IVF and product quantisation

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Vector search | Medium |

## Question

Explain IVF indexes and product quantisation (PQ), and when you'd choose them over HNSW.

## Answer

- IVF (inverted file): cluster the vectors with k-means into `nlist` centroids and assign each vector to its nearest centroid. At query time, search only the `nprobe` closest clusters. More probes give better recall and more latency.
- PQ (product quantisation): split each vector into m sub-vectors and replace each with the id of its nearest codebook centroid (for example 8 bits). A 768-dimension float32 vector (3 KB) compresses to tens of bytes, and distances are approximated with lookup tables.
- IVF-PQ combines both, which is the standard for billion-scale search in FAISS. Rerank the top candidates with full-precision vectors to recover accuracy.

Choose IVF-PQ when memory dominates (hundreds of millions of vectors or more) and a small recall loss is acceptable. Choose HNSW when you need top recall and low latency and the memory fits. Other options are scalar quantisation (int8) and binary quantisation with rescoring, which many managed services offer.

## Likely follow-ups

- Why do you need a training step for IVF-PQ but not for HNSW?

---

[← Q0222](../../batch_03_rag_retrieval/0222_hnsw_explained/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0224 →](../../batch_03_rag_retrieval/0224_measure_ann_recall_against_exact_search/README.md)

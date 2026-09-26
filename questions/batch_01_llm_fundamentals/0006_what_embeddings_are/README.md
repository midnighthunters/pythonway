# Q0006 · What embeddings are

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Embeddings | Easy |

## Question

What is an embedding, and what properties make embeddings useful for search and RAG?

## Answer

- An embedding is a fixed-length dense vector (for example 384 to 3,072 dimensions) produced by a model trained so that semantically similar inputs land close together.
- Token embeddings are the model's input lookup table. Sentence or document embeddings come from dedicated embedding models, usually trained contrastively on pairs of related texts.
- Similarity is usually cosine similarity or dot product on normalised vectors. Once vectors are unit length, the two are equivalent.

Useful properties:
- Semantic matching beyond keywords ("terminate contract" is close to "cancellation clause").
- Fixed size, so they can be indexed in approximate-nearest-neighbour structures such as HNSW and IVF.
- Cross-lingual and multimodal models put different languages or images in the same space.

Caveats: vectors from different embedding models (or versions) are not comparable, so re-embed on model change. Embeddings are weak at exact identifiers, numbers and negation ("not approved"), which is why hybrid search with BM25 helps. Embeddings can leak information about the source text, so treat them as sensitive data.

## Likely follow-ups

- Why must you re-index when you upgrade the embedding model?
- Why is negation hard for embedding similarity?

---

[← Q0005](../../batch_01_llm_fundamentals/0005_estimate_request_cost_from_token_usage/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0007 →](../../batch_01_llm_fundamentals/0007_cosine_similarity_and_top_k_with_numpy/README.md)

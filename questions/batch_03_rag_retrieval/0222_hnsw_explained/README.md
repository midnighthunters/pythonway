# Q0222 · HNSW explained

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Vector search | Medium |

## Question

Explain how HNSW approximate nearest-neighbour search works and which parameters you'd tune.

## Answer

- HNSW (Hierarchical Navigable Small World) builds a multi-layer proximity graph. Upper layers are sparse, with long-range links, and the bottom layer contains every vector with short-range links.
- Search starts at an entry point in the top layer and greedily moves to the neighbour closest to the query, drops down a layer, and repeats. On the bottom layer it runs a best-first search with a candidate list of size `ef_search`.
- Insertion assigns each vector a random top level and links it to its M nearest neighbours per layer.

Parameters:
- `M` (links per node): higher means better recall and more memory.
- `ef_construction`: higher means a better-quality graph but slower builds.
- `ef_search`: higher means better recall but slower queries. It is tunable per query, and it's the main recall/latency knob.

Properties: excellent recall and latency and supports incremental inserts, but it is memory-hungry (vectors plus graph), deletes are awkward (tombstones and rebuilds), and filtering needs care. It is used in pgvector, OpenSearch, Azure AI Search and most vector databases.

## Likely follow-ups

- How would you measure recall of an HNSW index in production?

---

[← Q0221](../../batch_03_rag_retrieval/0221_pre_filtering_versus_post_filtering/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0223 →](../../batch_03_rag_retrieval/0223_ivf_and_product_quantisation/README.md)

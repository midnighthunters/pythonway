# Q0265 · Scaling vector search to 100M chunks

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Infrastructure | Hard |

## Question

The corpus will grow to 100M chunks with 500 QPS peak. What do you change?

## Answer

- Memory maths first: 100M × 1,024 dimensions × 4 bytes is about 410 GB for the raw float32 vectors, plus the HNSW graph overhead. Options include quantisation (int8 or binary with rescoring, PQ), shorter Matryoshka dimensions, and disk-based ANN (DiskANN-style indexes).
- Sharding: partition by tenant, business line or document domain, so most queries hit a subset of shards. Scatter-gather across shards with per-shard top k.
- Replicas for QPS and availability, and autoscaling on query load.
- Filtering at scale: partition by high-cardinality security domains, and use filtered-ANN support that stays efficient under selective filters.
- Caching: query-embedding cache, hot-result cache (scoped by entitlements).
- Ingestion: streaming updates through a queue, bulk-load backfills, and background compaction and merges.
- Tiering: hot recent content on fast nodes, archives on cheaper tiers or separate indexes queried on demand.
- Measure recall versus latency continuously on sampled queries, since index parameters drift in behaviour as data grows.

## Likely follow-ups

- Where does the quantisation recall loss show up, and how do you compensate?

---

[← Q0264](../../batch_03_rag_retrieval/0264_pgvector_for_rag/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0266 →](../../batch_03_rag_retrieval/0266_sharding_and_replicas_for_search/README.md)

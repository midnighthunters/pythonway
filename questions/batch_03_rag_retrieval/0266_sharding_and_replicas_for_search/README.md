# Q0266 · Sharding and replicas for search

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Infrastructure | Medium |

## Question

Explain shards and replicas in a search cluster, and how they affect RAG latency, throughput and availability.

## Answer

- Shards split the index horizontally. Each holds part of the data, so a query fans out to all relevant shards and merges their top-k lists. More shards give parallelism for large indexes, but the fan-out overhead and tail latency grow (the slowest shard dominates p99).
- Replicas are copies of each shard. They add query throughput (load spread across copies) and availability (survive node loss), and cost storage and indexing work.

Guidance:
- Size shards by data volume and memory (vector indexes are memory-heavy). Avoid many tiny shards.
- Use routing or partitioning (by tenant or domain) so queries touch fewer shards.
- Put replicas across availability zones, and use more replicas for read-heavy RAG workloads.
- Watch p99 latency per shard, garbage-collection pauses, and hot shards caused by skewed tenants.

## Likely follow-ups

- Why does adding shards sometimes make p99 latency worse?

---

[← Q0265](../../batch_03_rag_retrieval/0265_scaling_vector_search_to_100m_chunks/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0267 →](../../batch_03_rag_retrieval/0267_rag_latency_budget/README.md)

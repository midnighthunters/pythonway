# Q0263 · OpenSearch hybrid retrieval

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Cloud AI services | Medium |

## Question

How would you implement hybrid retrieval in OpenSearch for RAG?

## Answer

- The index mapping has a `text` field with suitable analysers (language, synonyms), a `knn_vector` field (HNSW via the Lucene or FAISS engines, with the chosen space type), and keyword or date fields for filters (ACL groups, jurisdiction, effective date).
- The query uses a `hybrid` query combining a `match` or `multi_match` BM25 clause and a `knn` clause, each with filters. A search pipeline with a normalisation processor (min-max or L2, with weights), or RRF in newer versions, fuses the scores.
- Filtering: apply the ACL and metadata filters inside the k-NN query (efficient filtered search) rather than as a post-filter.
- Reranking: a reranking processor calling a cross-encoder model, or rerank in your application.
- Operations: shard sizing (the vector memory footprint), replicas for QPS, UltraWarm or cold tiers for old data, snapshots, and fine-grained access control.

Amazon OpenSearch Service and OpenSearch Serverless (vector collections) are the managed options on AWS.

## Likely follow-ups

- How do you size memory for 20M 1,024-dimensional HNSW vectors?

---

[← Q0262](../../batch_03_rag_retrieval/0262_amazon_bedrock_knowledge_bases/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0264 →](../../batch_03_rag_retrieval/0264_pgvector_for_rag/README.md)

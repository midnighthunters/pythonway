# Q0260 · Choosing a vector store

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Infrastructure | Medium |

## Question

How would you choose between pgvector, OpenSearch, Azure AI Search, a managed vector database and Bedrock Knowledge Bases for an enterprise RAG platform?

## Answer

Criteria:
- Retrieval features: hybrid (BM25 plus vector) in one query, filtered ANN performance, reranking integration, and multi-vector support.
- Security: private networking, encryption with customer-managed keys, fine-grained access control, and compliance approvals in the bank's cloud environment.
- Scale and performance: vector count, QPS, p99 latency, and update rate (real-time versus batch).
- Operations: managed versus self-run, backup and restore, multi-region, monitoring, and cost model.
- Ecosystem fit: existing skills and platforms (Postgres, OpenSearch clusters, Azure or AWS services), and SDK support in LangChain and LlamaIndex.

Rough fits:
- pgvector: moderate scale, and transactional data alongside vectors with SQL filters.
- OpenSearch or Elasticsearch: mature BM25 plus k-NN, large scale, strong filtering.
- Azure AI Search: managed hybrid search with a semantic ranker and integrated vectorisation in Azure.
- Bedrock Knowledge Bases: managed ingestion and retrieval in AWS, fastest to start, with less control.

## Likely follow-ups

- What would make you run two different stores in one platform?

---

[← Q0259](../../batch_03_rag_retrieval/0259_migrate_to_a_new_embedding_model/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0261 →](../../batch_03_rag_retrieval/0261_azure_ai_search_for_rag/README.md)

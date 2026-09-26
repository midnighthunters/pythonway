# Q0261 · Azure AI Search for RAG

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Cloud AI services | Medium |

## Question

What features of Azure AI Search matter for RAG on an Azure-based platform?

## Answer

- Hybrid queries: full-text (BM25) plus vector queries in one request, fused with reciprocal rank fusion.
- A semantic ranker: an optional transformer-based reranking of the top results, plus captions and highlights.
- Vector support: HNSW or exhaustive k-NN, with filters on the metadata fields, and vector compression options (scalar or binary quantisation) to reduce cost.
- Integrated vectorisation and indexers: pull from Blob Storage, SharePoint and databases, run skillsets (chunking, OCR, embedding with Azure OpenAI) on a schedule.
- Security: private endpoints, managed identities and Entra ID role-based access, customer-managed keys, and document-level security filters. You typically store ACL fields and filter on them at query time.
- Agentic retrieval and knowledge-source features have been added over time. Check the current feature set and regional availability, as these evolve.

Design points: index schema (filterable fields for ACLs, jurisdiction and dates), replica and partition sizing for QPS and storage, and quota planning for embedding calls during indexing.

## Likely follow-ups

- How would you implement security trimming with Entra ID groups in Azure AI Search?

---

[← Q0260](../../batch_03_rag_retrieval/0260_choosing_a_vector_store/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0262 →](../../batch_03_rag_retrieval/0262_amazon_bedrock_knowledge_bases/README.md)

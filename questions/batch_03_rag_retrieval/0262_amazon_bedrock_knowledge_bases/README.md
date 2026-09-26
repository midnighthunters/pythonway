# Q0262 · Amazon Bedrock Knowledge Bases

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Cloud AI services | Medium |

## Question

What does Amazon Bedrock Knowledge Bases provide, and what are the trade-offs versus building your own RAG pipeline?

## Answer

It provides:
- Managed ingestion from S3 and other connectors, with chunking strategies (fixed, hierarchical, semantic, or a custom Lambda), parsing options, embedding with Bedrock models, and storage in a supported vector store (for example OpenSearch Serverless, Aurora PostgreSQL with pgvector, and others).
- A `Retrieve` API (returns chunks) and `RetrieveAndGenerate` (managed RAG with citations), metadata filtering, optional reranking, and hybrid search on supported stores.
- Integration with Bedrock Agents and AgentCore, and Guardrails, plus IAM, KMS and VPC controls.

Trade-offs:
- Faster to launch, with less undifferentiated plumbing and managed scaling.
- Less control over parsing, chunking details, fusion and prompt construction. You also need your entitlement model to map onto metadata filters, and the product feature set and regions change over time.
- Model-agnostic platforms often use `Retrieve` only and do generation through their own gateway, so prompts, logging and routing stay consistent across Azure and AWS.

## Likely follow-ups

- Why might you use Retrieve but not RetrieveAndGenerate?

---

[← Q0261](../../batch_03_rag_retrieval/0261_azure_ai_search_for_rag/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0263 →](../../batch_03_rag_retrieval/0263_opensearch_hybrid_retrieval/README.md)

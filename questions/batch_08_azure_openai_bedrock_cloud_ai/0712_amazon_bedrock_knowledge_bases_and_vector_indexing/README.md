# Q0712 · Amazon Bedrock Knowledge Bases and vector indexing

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

What is Amazon Bedrock Knowledge Bases, and how does it implement fully managed RAG for enterprise documents?

## Answer

Amazon Bedrock Knowledge Bases is a managed RAG service that automates the end-to-end retrieval-augmented generation workflow:

Architecture:
1. Ingestion Pipeline:
   - Connects to data sources such as Amazon S3, Confluence, SharePoint, or Salesforce.
   - Automatically parses documents (PDF, DOCX, Markdown, CSV, HTML), applies chunking strategies (fixed-size, hierarchical parent-child, or semantic chunking), and generates embeddings via Amazon Titan Text Embeddings or Cohere Embed.
2. Vector Store Storage:
   - Stores and indexes vectors in managed vector databases: OpenSearch Serverless, Amazon Aurora PostgreSQL with `pgvector`, Pinecone, or Redis Enterprise.
3. Retrieval & Generation:
   - Exposes `Retrieve` (returns raw ranked passages with similarity scores) and `RetrieveAndGenerate` (retrieves passages and synthesizes an answer with inline citations using Claude or Titan).
4. Enterprise Security:
   - Inherits S3 and KMS encryption, with fine-grained IAM data access policies.

## Likely follow-ups

- What chunking strategy is best suited for complex corporate financial reports with balance sheet tables?
- How does Knowledge Bases handle document updates and deletions in the S3 bucket?

---

[← Q0711](../../batch_08_azure_openai_bedrock_cloud_ai/0711_amazon_bedrock_guardrails_and_pii_masking/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0713 →](../../batch_08_azure_openai_bedrock_cloud_ai/0713_amazon_bedrock_agents_and_agentcore/README.md)

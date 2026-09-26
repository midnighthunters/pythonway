# Q0771 · Knowledge Bases hybrid search: BM25 plus OpenSearch vector similarity

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

How does Amazon Bedrock Knowledge Bases combine lexical keyword search (BM25) with dense vector semantic search in OpenSearch Serverless?

## Answer

Limitations of Pure Vector Search:
- Vector embeddings excel at semantic concepts ("how to hedge currency risk"), but frequently fail on exact financial alphanumeric keywords, such as ISIN numbers (`US0378331005`), ticker symbols (`JPM`), or exact legal entity names.

Hybrid Search in Bedrock Knowledge Bases:
1. Dual Indexing in OpenSearch Serverless:
   - Each document passage is indexed simultaneously as a dense vector (via Titan Embeddings) and as an inverted BM25 text index.
2. Parallel Retrieval:
   - Lexical Search: BM25 scores exact keyword frequency and term inverse document frequency.
   - Dense Vector Search: Computes cosine similarity or dot product in high-dimensional space.
3. Score Normalization & Fusion:
   - Results are blended using Reciprocal Rank Fusion (RRF) or weighted linear combination:
     `FinalScore = (\alpha \times NormalizedVectorScore) + ((1 - \alpha) \times NormalizedBM25Score)`
4. Result: Captures both semantic meaning and exact keyword precision.

## Likely follow-ups

- What tuning value of $\alpha$ is recommended for financial compliance documents?
- How does OpenSearch Serverless handle vector index compaction without downtime?

---

[← Q0770](../../batch_08_azure_openai_bedrock_cloud_ai/0770_evaluating_hallucination_scores_against_ground_truth/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0772 →](../../batch_08_azure_openai_bedrock_cloud_ai/0772_reciprocal_rank_fusion_for_bedrock_knowledge_bases/README.md)

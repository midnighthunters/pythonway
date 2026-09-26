# Q0206 · Choosing a chunk size

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Chunking | Medium |

## Question

How do you choose the chunk size and overlap for an enterprise corpus?

## Answer

Trade-offs:
- Small chunks (100–300 tokens) give precise matches and less noise in the prompt, but lose context, and answers spanning several chunks need more of them.
- Large chunks (500–1,500 tokens) keep more context per hit, but their embeddings are "blurred" across topics, and they cost more prompt tokens per retrieved chunk.

Factors: document structure (FAQs and policies suit small chunks, narrative reports larger ones), the embedding model's input limit and training distribution, typical question granularity, and the reranker and context budget.

Process: start with structure-aware chunks of about 300–500 tokens with 10–15% overlap. Then measure recall@k and answer quality on a labelled question set across two or three sizes. Consider parent-child retrieval to get precise matching with larger context. Re-evaluate when the embedding model changes.

## Likely follow-ups

- What metric would convince you that chunks are too large?

---

[← Q0205](../../batch_03_rag_retrieval/0205_structure_aware_chunking_of_markdown/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0207 →](../../batch_03_rag_retrieval/0207_parent_child_retrieval/README.md)

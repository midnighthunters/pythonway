# Q0051 · Bi-encoders versus cross-encoders

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Embeddings | Medium |

## Question

Compare bi-encoders and cross-encoders for retrieval, and explain why production RAG usually uses both.

## Answer

- A bi-encoder embeds the query and each document separately, and scores them with a dot product. Document vectors are precomputed and indexed, so search over millions of documents takes milliseconds. Quality is limited, because the query and document never interact inside the model.
- A cross-encoder (reranker) feeds the query and document together through the model and outputs a relevance score. Full cross-attention between them makes it much more accurate, but it costs one model pass per pair and can't be precomputed.
- Standard pipeline: a bi-encoder (plus BM25) retrieves the top 50–200 candidates, then a cross-encoder reranks them to the top 5–10 that go into the prompt.
- Late-interaction models such as ColBERT sit in between: token-level vectors with MaxSim scoring give better quality than bi-encoders, at a larger index cost.

An LLM can also act as a reranker ("listwise" reranking). It is accurate, but expensive and slow, so use it only on small candidate sets.

## Likely follow-ups

- How would you measure whether the reranker is worth its latency?

---

[← Q0050](../../batch_01_llm_fundamentals/0050_knowledge_distillation/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0052 →](../../batch_01_llm_fundamentals/0052_matryoshka_embedding_truncation/README.md)

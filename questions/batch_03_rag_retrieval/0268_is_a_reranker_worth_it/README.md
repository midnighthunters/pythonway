# Q0268 · Is a reranker worth it

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Reranking | Medium |

## Question

How do you decide whether adding a cross-encoder reranker is worth its latency and cost?

## Answer

Measure it:
- Offline: run the golden set with and without reranking. Compare hit rate@k and nDCG at the k you actually send to the model (for example top 5), and final answer quality or groundedness.
- Online: track p95 latency added, cost per query, and user feedback or citation clicks in an A/B test.

It is usually worth it when first-stage retrieval has decent recall@50 but mediocre precision@5, when many near-duplicate or boilerplate chunks crowd the top results, and when context is expensive (large prompts, long answers).

It is less valuable when the corpus is small and clean, when queries are mostly identifier lookups (BM25 already nails them), or when you can afford to send many chunks to a long-context model anyway.

Tuning: candidates reranked (N = 20–100), kept (n = 3–10), model size, batching, and a timeout fallback to first-stage order.

## Likely follow-ups

- What would you do if the reranker helps English queries but hurts other languages?

---

[← Q0267](../../batch_03_rag_retrieval/0267_rag_latency_budget/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0269 →](../../batch_03_rag_retrieval/0269_late_interaction_maxsim_scoring/README.md)

# Q0061 · Choosing an embedding model

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Embeddings | Medium |

## Question

How would you choose an embedding model for enterprise search over policies, contracts and emails?

## Answer

Criteria:
- Retrieval quality on your data: build 100–300 labelled queries and measure recall@k and nDCG. Public leaderboards (MTEB) are only a starting shortlist.
- Domain and language coverage: legal and finance vocabulary, multilingual needs, code.
- Maximum input length versus your chunk size, and dimension versus storage cost (Matryoshka or `dimensions` support).
- Deployment and data controls: available in your approved cloud region (for example on Azure OpenAI or Bedrock), or self-hostable. Check data-retention terms.
- Throughput, latency and cost for both the initial backfill and incremental updates.
- Stability: versioning, deprecation policy, and the cost of re-embedding the whole corpus on change.

Then test hybrid search (BM25 plus vectors) with a reranker. The combination often matters more than the choice of embedding model.

## Likely follow-ups

- How would you migrate 50M chunks to a new embedding model without downtime (dual indexes, backfill, shadow queries)?

---

[← Q0060](../../batch_01_llm_fundamentals/0060_budget_max_tokens_against_the_context_window/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0062 →](../../batch_01_llm_fundamentals/0062_how_vision_language_models_see_images/README.md)

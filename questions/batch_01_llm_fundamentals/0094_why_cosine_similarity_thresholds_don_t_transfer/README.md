# Q0094 · Why cosine similarity thresholds don't transfer

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Embeddings | Medium |

## Question

A teammate hard-codes "treat similarity above 0.8 as relevant" for a semantic cache. Why is that fragile, and how should the threshold be chosen?

## Answer

- Score distributions differ by embedding model, version, dimension and domain. One model's unrelated pairs may sit around 0.7 while another's sit near 0.1. Upgrading the model silently changes what 0.8 means.
- Similarity is not relevance or equivalence. Two queries can be very similar ("transfer $500 to savings" versus "transfer $5,000 to savings") yet need different answers. That is dangerous for a semantic cache.
- Short queries, boilerplate and templated text push scores up.

Better practice:
- Choose thresholds from labelled pairs, for example the threshold that gives 99% precision on "same answer" pairs for a cache, and re-fit per model version.
- For caches, add guards: exact match on key entities and numbers, tenant and permission scope in the key, TTLs, and never cache personalised or entitlement-dependent answers across users.
- Monitor the hit rate and the false-hit rate with sampled review.

## Likely follow-ups

- How would you detect that a semantic cache is serving wrong answers?

---

[← Q0093](../../batch_01_llm_fundamentals/0093_memory_needed_to_fine_tune/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0095 →](../../batch_01_llm_fundamentals/0095_how_tool_calling_works_under_the_hood/README.md)

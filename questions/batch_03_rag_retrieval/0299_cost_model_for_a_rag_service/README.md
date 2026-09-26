# Q0299 · Cost model for a RAG service

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Cost engineering | Medium |

## Question

Build a per-query cost model for a RAG service (query embedding, reranking, LLM input and output tokens, with an answer-cache hit rate), and compute the monthly cost for a given volume.

## Answer

```python
from decimal import Decimal

M = Decimal(1_000_000)


def rag_cost_per_query(prompt_tokens: int, output_tokens: int, in_price: Decimal, out_price: Decimal,
                       query_embed_tokens: int, embed_price: Decimal, rerank_price_per_query: Decimal,
                       cache_hit_rate: Decimal) -> Decimal:
    llm = (prompt_tokens * in_price + output_tokens * out_price) / M
    embed = query_embed_tokens * embed_price / M
    full = embed + rerank_price_per_query + llm
    return (embed + (1 - cache_hit_rate) * (rerank_price_per_query + llm)).quantize(Decimal("0.000001")) \
        if cache_hit_rate else full.quantize(Decimal("0.000001"))


per_query = rag_cost_per_query(prompt_tokens=6_000, output_tokens=400, in_price=Decimal("2.50"),
                               out_price=Decimal("10.00"), query_embed_tokens=30, embed_price=Decimal("0.10"),
                               rerank_price_per_query=Decimal("0.001"), cache_hit_rate=Decimal("0"))
assert per_query == Decimal("0.020003")
cached = rag_cost_per_query(6_000, 400, Decimal("2.50"), Decimal("10.00"), 30, Decimal("0.10"),
                            Decimal("0.001"), Decimal("0.2"))
assert cached == Decimal("0.016003")
monthly = per_query * 200_000 * 22
assert monthly == Decimal("88013.200000")
```

The prices are illustrative. The embedding cost is paid even on cache hits, because you embed the query to look it up. Prompt tokens dominate: 6,000 input tokens at these rates is 75% of the cost. So the biggest levers are fewer or shorter chunks (better reranking), prompt caching of the stable prefix, smaller models for easy questions, and answer caching. Add fixed costs (the search cluster, ingestion and re-embedding) for the full picture.

## Likely follow-ups

- How would the numbers change with prompt caching on a 2,000-token system prompt?

---

[← Q0298](../../batch_03_rag_retrieval/0298_rag_failure_mode_checklist/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0300 →](../../batch_03_rag_retrieval/0300_design_entitlement_aware_enterprise_rag_for_llm_suite/README.md)

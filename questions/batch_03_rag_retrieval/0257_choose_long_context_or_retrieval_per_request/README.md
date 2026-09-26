# Q0257 · Choose long context or retrieval per request

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Routing | Medium |

## Question

Write a policy function that picks a strategy per request: whole-document prompting when a single document fits comfortably, map-reduce when a single document is too big, and retrieval for corpus-wide questions.

## Answer

```python
def choose_strategy(scope: str, doc_tokens: int | None, context_window: int, reserved_output: int,
                    overhead_tokens: int = 2_000, max_fraction: float = 0.6) -> str:
    if scope == "corpus":
        return "retrieve"
    if scope != "single_document" or doc_tokens is None:
        raise ValueError("scope must be 'corpus' or 'single_document' with a token count")
    usable = (context_window - reserved_output - overhead_tokens) * max_fraction
    return "whole_document" if doc_tokens <= usable else "map_reduce"


assert choose_strategy("corpus", None, 128_000, 4_000) == "retrieve"
assert choose_strategy("single_document", 40_000, 128_000, 4_000) == "whole_document"
assert choose_strategy("single_document", 90_000, 128_000, 4_000) == "map_reduce"
```

`max_fraction` keeps a safety margin because quality and latency degrade near the limit, and a very long prefill is slow and costly. Tune it with evaluations per model. Cost matters too: a 90k-token prompt repeated for every follow-up question is expensive unless prompt caching applies.

## Likely follow-ups

- How does prompt caching change this decision for multi-turn chat over one document?

---

[← Q0256](../../batch_03_rag_retrieval/0256_route_between_rag_and_sql/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0258 →](../../batch_03_rag_retrieval/0258_cache_embeddings_by_content_and_model/README.md)

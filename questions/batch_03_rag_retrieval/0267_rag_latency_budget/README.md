# Q0267 · RAG latency budget

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Latency engineering | Medium |

## Question

Write a latency-budget checker for a RAG request: stages with p95 latencies (some running in parallel) against per-stage budgets and an end-to-end time-to-first-token target. Report the total and any stage over budget.

## Answer

```python
def check_budget(stages: list[dict], ttft_target_ms: float) -> dict:
    """stages: {'name', 'parallel': [ms, ...] or 'ms', 'budget_ms'} in execution order, up to first token."""
    total, over = 0.0, []
    for s in stages:
        ms = max(s["parallel"]) if "parallel" in s else s["ms"]
        total += ms
        if ms > s["budget_ms"]:
            over.append(s["name"])
    return {"ttft_ms": total, "meets_target": total <= ttft_target_ms, "over_budget": over}


stages = [
    {"name": "condense", "ms": 250, "budget_ms": 300},
    {"name": "retrieve", "parallel": [60, 110], "budget_ms": 150},
    {"name": "rerank", "ms": 180, "budget_ms": 120},
    {"name": "llm_ttft", "ms": 700, "budget_ms": 900},
]
r = check_budget(stages, ttft_target_ms=1_500)
assert r == {"ttft_ms": 1240.0, "meets_target": True, "over_budget": ["rerank"]}
```

BM25 and vector search run in parallel, so only the slower one counts. Common levers: skip condensing on first turns, use a smaller reranker or fewer candidates, stream immediately, send a "searching…" status event, cache query embeddings, and co-locate services in the same region. Budget at p95, not the average, because RAG latency has long tails.

## Likely follow-ups

- Which stage would you move off the critical path first?

---

[← Q0266](../../batch_03_rag_retrieval/0266_sharding_and_replicas_for_search/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0268 →](../../batch_03_rag_retrieval/0268_is_a_reranker_worth_it/README.md)

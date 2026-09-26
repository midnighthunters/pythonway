# Q0086 · Pack texts into embedding batches

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Embedding pipelines | Medium |

## Question

An embedding API accepts at most N inputs and T total tokens per request. Write a function that packs chunks, in order, into the fewest sequential batches that respect both limits, and fails clearly on an oversized chunk.

## Answer

```python
def pack_batches(token_counts: list[int], max_items: int, max_tokens: int) -> list[list[int]]:
    batches: list[list[int]] = []
    cur: list[int] = []
    cur_tokens = 0
    for i, t in enumerate(token_counts):
        if t > max_tokens:
            raise ValueError(f"chunk {i} has {t} tokens, above the {max_tokens} limit; re-chunk it")
        if cur and (len(cur) == max_items or cur_tokens + t > max_tokens):
            batches.append(cur)
            cur, cur_tokens = [], 0
        cur.append(i)
        cur_tokens += t
    if cur:
        batches.append(cur)
    return batches


assert pack_batches([100, 200, 300, 400, 50], max_items=3, max_tokens=500) == [[0, 1], [2], [3, 4]]
assert pack_batches([1] * 5, max_items=2, max_tokens=100) == [[0, 1], [2, 3], [4]]
assert pack_batches([], 10, 10) == []
try:
    pack_batches([10, 600], 3, 500)
    raise AssertionError
except ValueError:
    pass
```

Production additions: keep chunk ids with each batch so results map back, retry with backoff on 429s, bound concurrency, make the backfill resumable (checkpoint completed batches), and record the embedding model version with every vector.

## Likely follow-ups

- How would you backfill 20M chunks within a tokens-per-minute quota?

---

[← Q0085](../../batch_01_llm_fundamentals/0085_agent_latency_budget_with_parallel_stages/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0087 →](../../batch_01_llm_fundamentals/0087_batch_inference_apis_for_offline_workloads/README.md)

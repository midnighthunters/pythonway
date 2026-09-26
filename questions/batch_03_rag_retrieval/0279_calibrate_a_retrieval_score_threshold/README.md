# Q0279 · Calibrate a retrieval score threshold

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Reliability | Medium |

## Question

Given labelled (score, relevant) pairs from the reranker, choose the lowest threshold that achieves a target precision, and report the recall at that threshold.

## Answer

```python
def pick_threshold(pairs: list[tuple[float, bool]], target_precision: float) -> tuple[float, float] | None:
    total_relevant = sum(r for _, r in pairs)
    for t in sorted({s for s, _ in pairs}):
        kept = [r for s, r in pairs if s >= t]
        if kept and sum(kept) / len(kept) >= target_precision:
            recall = sum(kept) / total_relevant if total_relevant else 0.0
            return t, recall
    return None


pairs = [(0.95, True), (0.9, True), (0.8, True), (0.7, False), (0.65, True), (0.6, False), (0.4, False), (0.3, True)]
t, recall = pick_threshold(pairs, 0.8)
assert t == 0.65 and recall == 0.8
assert pick_threshold(pairs, 1.0) == (0.8, 0.6)
assert pick_threshold([(0.5, False)], 0.9) is None
```

Scanning thresholds from low to high, the first one that meets the precision target keeps the most recall. Use enough labelled pairs from real queries (hundreds or more), recalibrate when the reranker or corpus changes, and consider separate thresholds per query type.

## Likely follow-ups

- Why might precision not increase monotonically as the threshold rises?

---

[← Q0278](../../batch_03_rag_retrieval/0278_abstain_when_retrieval_is_weak/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0280 →](../../batch_03_rag_retrieval/0280_collapse_near_identical_hits_across_documents/README.md)

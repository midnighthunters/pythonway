# Q0278 · Abstain when retrieval is weak

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Reliability | Medium |

## Question

Implement a gate before generation: abstain if nothing was retrieved or the best rerank score is below a threshold. Otherwise pass through only the chunks within a margin of the best score.

## Answer

```python
def retrieval_gate(hits: list[dict], min_score: float, margin: float) -> dict:
    if not hits:
        return {"action": "abstain", "reason": "no_results", "chunks": []}
    best = max(h["score"] for h in hits)
    if best < min_score:
        return {"action": "abstain", "reason": "low_confidence", "chunks": []}
    keep = [h for h in hits if h["score"] >= best - margin]
    return {"action": "generate", "reason": "ok", "chunks": sorted(keep, key=lambda h: -h["score"])}


hits = [{"id": "a", "score": 0.82}, {"id": "b", "score": 0.77}, {"id": "c", "score": 0.31}]
assert [h["id"] for h in retrieval_gate(hits, 0.5, 0.1)["chunks"]] == ["a", "b"]
assert retrieval_gate([{"id": "x", "score": 0.2}], 0.5, 0.1)["reason"] == "low_confidence"
assert retrieval_gate([], 0.5, 0.1)["reason"] == "no_results"
```

Thresholds must be calibrated per reranker or model version (raw scores aren't portable). An abstention should still help the user: suggest rephrasing, related documents, or a human contact.

## Likely follow-ups

- What's the cost of setting `min_score` too high?

---

[← Q0277](../../batch_03_rag_retrieval/0277_compare_chunking_strategies_with_an_evaluation/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0279 →](../../batch_03_rag_retrieval/0279_calibrate_a_retrieval_score_threshold/README.md)

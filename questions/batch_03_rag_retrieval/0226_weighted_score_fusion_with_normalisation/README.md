# Q0226 · Weighted score fusion with normalisation

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Hybrid search | Medium |

## Question

Implement weighted hybrid fusion: min-max normalise each retriever's scores, treat missing documents as 0, and combine with a weight α for BM25. Show how α changes the winner.

## Answer

```python
def minmax(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return {}
    lo, hi = min(scores.values()), max(scores.values())
    if hi == lo:
        return {d: 1.0 for d in scores}
    return {d: (s - lo) / (hi - lo) for d, s in scores.items()}


def weighted_fusion(bm25: dict[str, float], vec: dict[str, float], alpha: float) -> list[str]:
    nb, nv = minmax(bm25), minmax(vec)
    docs = nb.keys() | nv.keys()
    combined = {d: alpha * nb.get(d, 0.0) + (1 - alpha) * nv.get(d, 0.0) for d in docs}
    return sorted(combined, key=lambda d: (-combined[d], d))


bm25 = {"id-match": 12.0, "semantic": 3.0, "noise": 1.0}
vec = {"semantic": 0.83, "id-match": 0.60, "noise": 0.59}
assert weighted_fusion(bm25, vec, alpha=0.7)[0] == "id-match"
assert weighted_fusion(bm25, vec, alpha=0.2)[0] == "semantic"
```

Tune α on labelled queries, possibly per query type (identifier-like queries favour BM25). Min-max normalisation is sensitive to outliers and to how many results each retriever returns, which is one reason RRF is the safer default.

## Likely follow-ups

- How could you choose α dynamically per query?

---

[← Q0225](../../batch_03_rag_retrieval/0225_reciprocal_rank_fusion/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0227 →](../../batch_03_rag_retrieval/0227_rerank_candidates_with_a_fallback/README.md)

# Q0225 · Reciprocal rank fusion

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Hybrid search | Easy |

## Question

Implement reciprocal rank fusion (RRF) to combine BM25 and vector result lists, and explain why it's popular for hybrid search.

## Answer

RRF score = Σ over lists of 1 / (k + rank), with k typically 60. It uses only ranks, not raw scores.

```python
from collections import defaultdict


def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, doc in enumerate(ranking, start=1):
            scores[doc] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: (-x[1], x[0]))


bm25 = ["pol-7", "faq-2", "pol-9"]
vector = ["faq-2", "pol-3", "pol-7"]
fused = rrf([bm25, vector])
assert [d for d, _ in fused][:2] == ["faq-2", "pol-7"]
assert abs(dict(fused)["faq-2"] - (1 / 62 + 1 / 61)) < 1e-12
assert [d for d, _ in rrf([["a"], ["b", "a"]])][0] == "a"
```

Why it's popular: BM25 and cosine scores live on incomparable scales, and RRF sidesteps normalisation entirely. It is robust, has one parameter, and rewards documents that several retrievers agree on. Azure AI Search and OpenSearch offer it natively for hybrid queries.

Weakness: it discards score magnitudes, so a very strong single-retriever match can be outvoted by mediocre consensus.

## Likely follow-ups

- When would weighted score fusion beat RRF?

---

[← Q0224](../../batch_03_rag_retrieval/0224_measure_ann_recall_against_exact_search/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0226 →](../../batch_03_rag_retrieval/0226_weighted_score_fusion_with_normalisation/README.md)

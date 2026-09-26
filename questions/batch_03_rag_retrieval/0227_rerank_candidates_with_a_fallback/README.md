# Q0227 · Rerank candidates with a fallback

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Reranking | Medium |

## Question

Implement a reranking step: score the top-N candidates with a cross-encoder (a batched function), keep the top n, break ties by the original rank, and fall back to the original order if the reranker times out or fails.

## Answer

```python
from typing import Callable


def rerank(query: str, candidates: list[dict], scorer: Callable[[str, list[str]], list[float]],
           top_n: int, max_candidates: int = 50) -> tuple[list[dict], bool]:
    pool = candidates[:max_candidates]
    try:
        scores = scorer(query, [c["text"] for c in pool])
        if len(scores) != len(pool):
            raise ValueError("scorer returned wrong number of scores")
    except (TimeoutError, ValueError):
        return pool[:top_n], False
    order = sorted(range(len(pool)), key=lambda i: (-scores[i], i))
    return [pool[i] for i in order[:top_n]], True


cands = [{"id": "a", "text": "hotel booking portal"}, {"id": "b", "text": "London hotel cap is 180 GBP"},
         {"id": "c", "text": "flight rules"}]


def fake_cross_encoder(q: str, texts: list[str]) -> list[float]:
    return [sum(w in t.lower() for w in q.lower().split()) for t in texts]


out, used = rerank("london hotel cap", cands, fake_cross_encoder, top_n=2)
assert used and [c["id"] for c in out] == ["b", "a"]


def slow(q, texts):
    raise TimeoutError


out, used = rerank("london hotel cap", cands, slow, top_n=2)
assert not used and [c["id"] for c in out] == ["a", "b"]
```

Rerankers usually give the biggest precision gain per millisecond in RAG. Budget their latency (a batch of 50 pairs on a GPU is typically tens of milliseconds, and hosted rerank APIs such as Cohere, or those available through Bedrock and Azure, add network time), and always keep a fallback path.

## Likely follow-ups

- How do you pick N (candidates reranked) and n (kept)?

---

[← Q0226](../../batch_03_rag_retrieval/0226_weighted_score_fusion_with_normalisation/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0228 →](../../batch_03_rag_retrieval/0228_condense_follow_up_questions/README.md)

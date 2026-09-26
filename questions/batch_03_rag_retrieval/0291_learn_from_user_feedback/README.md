# Q0291 · Learn from user feedback

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Continuous improvement | Medium |

## Question

Users give thumbs up or down on answers. Aggregate feedback per chunk used in the answer (with smoothing), and flag chunks that are frequently involved in bad answers for review.

## Answer

```python
from collections import defaultdict


def chunk_feedback(events: list[dict], min_votes: int = 5, bad_threshold: float = 0.35) -> dict:
    up, n = defaultdict(int), defaultdict(int)
    for e in events:
        for cid in set(e["chunk_ids"]):
            n[cid] += 1
            up[cid] += e["thumbs_up"]
    scores = {cid: (up[cid] + 1) / (n[cid] + 2) for cid in n}
    flagged = sorted(cid for cid, s in scores.items() if n[cid] >= min_votes and s < bad_threshold)
    return {"scores": scores, "flagged": flagged}


events = ([{"chunk_ids": ["old-policy"], "thumbs_up": False}] * 8 + [{"chunk_ids": ["old-policy"], "thumbs_up": True}]
          + [{"chunk_ids": ["pol-7", "pol-7"], "thumbs_up": True}] * 6 + [{"chunk_ids": ["rare"], "thumbs_up": False}])
res = chunk_feedback(events)
assert res["flagged"] == ["old-policy"]
assert abs(res["scores"]["pol-7"] - 7 / 8) < 1e-12 and "rare" not in res["flagged"]
```

Laplace smoothing stops a single vote from dominating. Feedback is noisy and biased (people rate the answer, not the chunk, and a correct but unwelcome answer gets a thumbs down), so use it to prioritise review and evaluation-set additions, not to auto-demote content. Owners should review flagged chunks: often the document is outdated.

## Likely follow-ups

- Why shouldn't you automatically demote chunks with poor feedback?

---

[← Q0290](../../batch_03_rag_retrieval/0290_rag_over_email_and_chat/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0292 →](../../batch_03_rag_retrieval/0292_monitoring_rag_in_production/README.md)

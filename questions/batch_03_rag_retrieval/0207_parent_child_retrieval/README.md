# Q0207 · Parent-child retrieval

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Retrieval patterns | Medium |

## Question

Implement "small-to-big" retrieval: index small child chunks for precise matching, but return their larger parent sections (deduplicated, ordered by the best child score) as context.

## Answer

```python
from typing import Callable


def parent_child_retrieve(query: str, children: list[dict], parents: dict[str, str],
                          score: Callable[[str, str], float], k_children: int = 5, k_parents: int = 2) -> list[str]:
    ranked = sorted(children, key=lambda c: score(query, c["text"]), reverse=True)[:k_children]
    out: list[str] = []
    for c in ranked:
        if score(query, c["text"]) <= 0:
            break
        if c["parent_id"] not in out:
            out.append(c["parent_id"])
        if len(out) == k_parents:
            break
    return [parents[p] for p in out]


def overlap(q: str, t: str) -> float:
    return len(set(q.lower().split()) & set(t.lower().split()))


parents = {"hotels": "HOTELS. London cap 180 GBP. Paris cap 160 EUR. Book via portal.",
           "flights": "FLIGHTS. Economy under 6 hours. Business over 6 hours with approval."}
children = [{"parent_id": "hotels", "text": "London cap 180 GBP"},
            {"parent_id": "hotels", "text": "Paris cap 160 EUR"},
            {"parent_id": "flights", "text": "Business over 6 hours with approval"}]
assert parent_child_retrieve("london hotel cap", children, parents, overlap, k_parents=2) == [parents["hotels"]]
assert parent_child_retrieve("business over 6 hours", children, parents, overlap)[0] == parents["flights"]
```

Parents can be sections or whole short documents. Watch the prompt budget, since several big parents fill it quickly. LangChain's `ParentDocumentRetriever` implements this pattern.

## Likely follow-ups

- When does returning the parent hurt answer quality?

---

[← Q0206](../../batch_03_rag_retrieval/0206_choosing_a_chunk_size/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0208 →](../../batch_03_rag_retrieval/0208_sentence_window_retrieval/README.md)

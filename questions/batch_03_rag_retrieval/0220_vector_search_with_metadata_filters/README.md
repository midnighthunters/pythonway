# Q0220 · Vector search with metadata filters

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Vector search | Medium |

## Question

Implement brute-force vector search that applies metadata filters (equality and set membership) before ranking, and returns the top k with scores.

## Answer

```python
import numpy as np


def matches(meta: dict, filters: dict) -> bool:
    for key, cond in filters.items():
        value = meta.get(key)
        if isinstance(cond, (set, frozenset)):
            if value not in cond:
                return False
        elif value != cond:
            return False
    return True


def filtered_search(query: np.ndarray, vectors: np.ndarray, metas: list[dict], filters: dict, k: int):
    idx = [i for i, m in enumerate(metas) if matches(m, filters)]
    if not idx:
        return []
    v = vectors[idx]
    scores = (v @ query) / (np.linalg.norm(v, axis=1) * np.linalg.norm(query) + 1e-12)
    order = np.argsort(-scores, kind="stable")[:k]
    return [(idx[j], float(scores[j])) for j in order]


vecs = np.array([[1, 0], [0.9, 0.1], [0, 1], [0.95, 0.05]], dtype=float)
metas = [{"jurisdiction": "UK", "type": "policy"}, {"jurisdiction": "US", "type": "policy"},
         {"jurisdiction": "UK", "type": "faq"}, {"jurisdiction": "UK", "type": "policy"}]
res = filtered_search(np.array([1.0, 0.0]), vecs, metas, {"jurisdiction": "UK", "type": {"policy", "faq"}}, 2)
assert [i for i, _ in res] == [0, 3]
assert filtered_search(np.array([1.0, 0.0]), vecs, metas, {"jurisdiction": "JP"}, 2) == []
```

Brute force is fine up to roughly 10^5–10^6 vectors. Beyond that, use an ANN index with native filter support.

## Likely follow-ups

- What breaks if the filter is very selective and you use an ANN index that filters after search?

---

[← Q0219](../../batch_03_rag_retrieval/0219_why_bm25_still_matters/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0221 →](../../batch_03_rag_retrieval/0221_pre_filtering_versus_post_filtering/README.md)

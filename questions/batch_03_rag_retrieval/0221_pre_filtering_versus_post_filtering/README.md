# Q0221 · Pre-filtering versus post-filtering

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Vector search | Medium |

## Question

Demonstrate why post-filtering (retrieve the top k, then filter) can return far fewer than k results, while pre-filtering returns k. What do real vector databases do about it?

## Answer

```python
import numpy as np

rng = np.random.default_rng(0)
vectors = rng.normal(size=(1000, 16))
allowed = np.zeros(1000, dtype=bool)
allowed[rng.choice(1000, size=30, replace=False)] = True
query = rng.normal(size=16)
scores = vectors @ query
k = 10

top_k = np.argsort(-scores)[:k]
post = [i for i in top_k if allowed[i]]
pre = [i for i in np.argsort(-scores) if allowed[i]][:k]

assert len(pre) == k
assert len(post) < k
assert set(post) <= set(pre)
```

With 3% of documents visible to this user, post-filtering the global top 10 leaves almost nothing. For entitlement filters, post-filtering is also a leakage risk if the unfiltered results are ever logged or exposed.

What vector databases do:
- Filtered ANN: HNSW traversal that only accepts filter-matching nodes, sometimes with adaptive strategies (pre-filter plus brute force when the filter is very selective).
- Over-fetching (retrieve k × m, then filter), which is a weak fallback.
- Partitioning by tenant or ACL group for hard isolation.

## Likely follow-ups

- Which strategy would you use for a user who can see only 0.1% of the corpus?

---

[← Q0220](../../batch_03_rag_retrieval/0220_vector_search_with_metadata_filters/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0222 →](../../batch_03_rag_retrieval/0222_hnsw_explained/README.md)

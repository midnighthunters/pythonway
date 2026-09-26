# Q0007 · Cosine similarity and top-k with NumPy

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Embeddings | Easy |

## Question

Implement batched cosine similarity between a query vector and a matrix of document vectors, and return the indices of the top-k documents. Handle zero vectors safely.

## Answer

Approach: L2-normalise the rows (guarding against zero norms), take a matrix-vector product, then use `argpartition` for O(n) top-k selection before sorting just those k.

```python
import numpy as np


def normalize(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norms = np.linalg.norm(x, axis=-1, keepdims=True)
    return x / np.maximum(norms, eps)


def top_k_cosine(query: np.ndarray, docs: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    scores = normalize(docs) @ normalize(query)
    k = min(k, len(scores))
    idx = np.argpartition(-scores, k - 1)[:k]
    idx = idx[np.argsort(-scores[idx], kind="stable")]
    return idx, scores[idx]


docs = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7], [0.0, 0.0], [-1.0, 0.0]])
idx, scores = top_k_cosine(np.array([1.0, 0.1]), docs, 2)
assert idx.tolist() == [0, 2]
assert np.isclose(scores[0], 1 / np.sqrt(1.01))
all_idx, _ = top_k_cosine(np.array([1.0, 0.0]), docs, 10)
assert len(all_idx) == 5 and all_idx[-1] == 4
```

Complexity: O(n·d) for the scores, O(n + k log k) for selection.

Production note: normalise once at index time and store unit vectors, so query time is a dot product. Beyond a few million vectors, use an ANN index instead of brute force.

## Likely follow-ups

- When is dot product preferable to cosine (models trained with un-normalised dot product)?
- How would you do this for 50 million vectors within 50 ms?

---

[← Q0006](../../batch_01_llm_fundamentals/0006_what_embeddings_are/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0008 →](../../batch_01_llm_fundamentals/0008_numerically_stable_softmax/README.md)

# Q0052 · Matryoshka embedding truncation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Embeddings | Medium |

## Question

Some embedding models are trained with Matryoshka representation learning, so a prefix of the vector is itself a good embedding. Implement truncation with renormalisation, and measure how well rankings are preserved.

## Answer

Why it matters here: shorter vectors (for example 3,072 → 256 dimensions) cut vector-store memory and search latency by an order of magnitude. Several hosted embedding APIs expose a `dimensions` parameter that relies on this property.

```python
import numpy as np


def truncate(vectors: np.ndarray, dims: int) -> np.ndarray:
    v = vectors[:, :dims]
    return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-12)


def overlap_at_k(full: np.ndarray, short: np.ndarray, query_idx: int, k: int) -> float:
    def top(m):
        s = m @ m[query_idx]
        s[query_idx] = -np.inf
        return set(np.argsort(-s)[:k])
    return len(top(full) & top(short)) / k


rng = np.random.default_rng(0)
# Simulate a Matryoshka-like space: most signal in the leading dimensions.
decay = np.exp(-np.arange(512) / 40)
docs = rng.normal(size=(300, 512)) * decay
full = truncate(docs, 512)
assert np.allclose(np.linalg.norm(truncate(docs, 64), axis=1), 1)
assert overlap_at_k(full, truncate(docs, 128), 0, 10) >= 0.8
assert overlap_at_k(full, truncate(docs, 128), 0, 10) >= overlap_at_k(full, truncate(docs, 8), 0, 10)
```

In production, pick the dimension by measuring recall@k on your own labelled queries, not on synthetic data. Renormalise after truncating, or cosine similarity scores will be wrong.

## Likely follow-ups

- What else reduces vector memory (int8 or binary quantisation, product quantisation)?

---

[← Q0051](../../batch_01_llm_fundamentals/0051_bi_encoders_versus_cross_encoders/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0053 →](../../batch_01_llm_fundamentals/0053_tokenization_cost_surprises/README.md)

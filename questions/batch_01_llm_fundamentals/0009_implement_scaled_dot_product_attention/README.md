# Q0009 · Implement scaled dot-product attention

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Medium |

## Question

Implement scaled dot-product attention `softmax(QKᵀ/√d_k + mask) V` in NumPy, with an optional boolean mask where `True` means "may attend".

## Answer

```python
import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    z = x - x.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def attention(q: np.ndarray, k: np.ndarray, v: np.ndarray, mask: np.ndarray | None = None):
    d_k = q.shape[-1]
    scores = q @ np.swapaxes(k, -1, -2) / np.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, scores, -1e9)
    weights = softmax(scores)
    return weights @ v, weights


rng = np.random.default_rng(0)
q, k, v = rng.normal(size=(4, 8)), rng.normal(size=(6, 8)), rng.normal(size=(6, 3))
out, w = attention(q, k, v)
assert out.shape == (4, 3) and np.allclose(w.sum(-1), 1)
only_first = np.zeros((4, 6), dtype=bool)
only_first[:, 0] = True
out, w = attention(q, k, v, only_first)
assert np.allclose(out, np.repeat(v[:1], 4, axis=0))
```

Shapes: Q is (n_q, d_k), K is (n_k, d_k), V is (n_k, d_v), and the output is (n_q, d_v). Cost is O(n_q · n_k · d), which is quadratic in sequence length for self-attention.

Intuition: each query computes a weighted average of the values, with weights given by how well it matches each key.

## Likely follow-ups

- Why use a large negative number instead of `-inf` in some implementations (NaN rows when everything is masked)?
- How does FlashAttention compute the same result without materialising the n×n matrix?

---

[← Q0008](../../batch_01_llm_fundamentals/0008_numerically_stable_softmax/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0010 →](../../batch_01_llm_fundamentals/0010_why_attention_scales_by_the_square_root_of_d_k/README.md)

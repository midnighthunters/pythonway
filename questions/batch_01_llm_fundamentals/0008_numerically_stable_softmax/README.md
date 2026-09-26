# Q0008 · Numerically stable softmax

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Math | Easy |

## Question

Implement softmax over the last axis that doesn't overflow for large logits, and log-softmax.

## Answer

Approach: softmax is invariant to subtracting a constant, so subtract the row maximum before `exp`. Log-softmax is `x - logsumexp(x)`, computed the same stable way.

```python
import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    z = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(z)
    return e / np.sum(e, axis=axis, keepdims=True)


def log_softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    z = x - np.max(x, axis=axis, keepdims=True)
    return z - np.log(np.sum(np.exp(z), axis=axis, keepdims=True))


logits = np.array([[1000.0, 1001.0, 1002.0], [1.0, 2.0, 3.0]])
p = softmax(logits)
assert np.all(np.isfinite(p))
assert np.allclose(p[0], p[1])
assert np.allclose(p.sum(axis=-1), 1.0)
assert np.allclose(np.exp(log_softmax(logits)), p)
```

The naive `np.exp(1000)` overflows to `inf`, and `inf/inf` gives `nan`.

## Likely follow-ups

- Why is log-softmax preferred for computing cross-entropy?
- What does temperature do to softmax mathematically?

---

[← Q0007](../../batch_01_llm_fundamentals/0007_cosine_similarity_and_top_k_with_numpy/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0009 →](../../batch_01_llm_fundamentals/0009_implement_scaled_dot_product_attention/README.md)

# Q0010 · Why attention scales by the square root of d_k

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Medium |

## Question

Why divide `QKᵀ` by `√d_k`? Demonstrate the effect numerically.

## Answer

If the entries of q and k are independent with zero mean and unit variance, `q·k` has variance `d_k`. For large `d_k` the logits have a large spread, so softmax saturates into an almost one-hot distribution and its gradients vanish. Dividing by `√d_k` keeps the variance around 1.

```python
import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    z = x - x.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


rng = np.random.default_rng(42)
d_k, n = 512, 16
q = rng.normal(size=(1000, d_k))
k = rng.normal(size=(n, d_k))
raw = q @ k.T
scaled = raw / np.sqrt(d_k)
assert 400 < raw.var() < 620
assert 0.8 < scaled.var() < 1.2
max_raw = softmax(raw).max(axis=-1).mean()
max_scaled = softmax(scaled).max(axis=-1).mean()
assert max_raw > 0.9 and max_scaled < 0.5
```

The unscaled softmax puts over 90% of the weight on one key (saturated). The scaled version stays spread out and trainable.

## Likely follow-ups

- How does temperature at decoding time relate to this idea?
- What other normalisation tricks stabilise attention (QK-norm)?

---

[← Q0009](../../batch_01_llm_fundamentals/0009_implement_scaled_dot_product_attention/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0011 →](../../batch_01_llm_fundamentals/0011_build_a_causal_attention_mask/README.md)

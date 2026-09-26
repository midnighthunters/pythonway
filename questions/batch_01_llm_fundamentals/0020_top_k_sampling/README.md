# Q0020 · Top-k sampling

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding | Easy |

## Question

Implement top-k sampling: keep only the k highest logits, renormalise and sample.

## Answer

```python
import numpy as np


def top_k_filter(logits: np.ndarray, k: int) -> np.ndarray:
    if k <= 0 or k >= len(logits):
        return logits.copy()
    kth = np.partition(logits, -k)[-k]
    return np.where(logits >= kth, logits, -np.inf)


def sample_top_k(logits: np.ndarray, k: int, rng: np.random.Generator) -> int:
    filtered = top_k_filter(logits, k)
    z = filtered - filtered.max()
    p = np.exp(z)
    p /= p.sum()
    return int(rng.choice(len(logits), p=p))


logits = np.array([3.0, 2.5, 0.1, -2.0, -3.0])
rng = np.random.default_rng(0)
samples = {sample_top_k(logits, 2, rng) for _ in range(500)}
assert samples == {0, 1}
assert np.isneginf(top_k_filter(logits, 2)[2:]).all()
```

`exp(-inf) = 0`, so filtered tokens get exactly zero probability.

Weakness: a fixed k is too many for peaked distributions (it admits junk) and too few for flat ones (it cuts off good options). Top-p adapts to the shape of the distribution.

Tie note: `>= kth` can keep more than k tokens when there are ties, which is usually acceptable.

## Likely follow-ups

- When would you combine top-k with top-p?

---

[← Q0019](../../batch_01_llm_fundamentals/0019_temperature_scaling/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0021 →](../../batch_01_llm_fundamentals/0021_top_p_nucleus_sampling/README.md)

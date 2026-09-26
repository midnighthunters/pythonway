# Q0014 · Rotary position embeddings

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Hard |

## Question

Implement RoPE for a single head and verify its key property: the dot product of a rotated query and key depends only on their relative distance.

## Answer

Approach: treat consecutive dimension pairs as 2-D points and rotate pair i at position p by angle `p · θ_i`, where `θ_i = base^(-2i/d)`. Rotations preserve norms, and `R(a)ᵀR(b) = R(b - a)`, so `⟨R_m q, R_n k⟩` depends only on `n - m`.

```python
import numpy as np


def rope(x: np.ndarray, positions: np.ndarray, base: float = 10000.0) -> np.ndarray:
    d = x.shape[-1]
    theta = base ** (-np.arange(0, d, 2) / d)
    ang = positions[:, None] * theta[None, :]
    cos, sin = np.cos(ang), np.sin(ang)
    x1, x2 = x[..., 0::2], x[..., 1::2]
    out = np.empty_like(x)
    out[..., 0::2] = x1 * cos - x2 * sin
    out[..., 1::2] = x1 * sin + x2 * cos
    return out


rng = np.random.default_rng(0)
q, k = rng.normal(size=8), rng.normal(size=8)


def score(m: int, n: int) -> float:
    return float(rope(q[None], np.array([m]))[0] @ rope(k[None], np.array([n]))[0])


assert np.isclose(score(3, 7), score(10, 14))
assert np.isclose(score(0, 5), score(100, 105))
assert not np.isclose(score(3, 7), score(3, 8))
assert np.isclose(np.linalg.norm(rope(q[None], np.array([42]))), np.linalg.norm(q))
```

Why it matters: RoPE is what most modern open models (Llama, Mistral, Qwen) use. Context-extension techniques such as position interpolation and YaRN work by rescaling these angles.

## Likely follow-ups

- Why does RoPE generalise poorly beyond the trained length without scaling?
- Where is RoPE applied: to Q and K only, or also to V?

---

[← Q0013](../../batch_01_llm_fundamentals/0013_sinusoidal_positional_encoding/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0015 →](../../batch_01_llm_fundamentals/0015_layernorm_versus_rmsnorm/README.md)

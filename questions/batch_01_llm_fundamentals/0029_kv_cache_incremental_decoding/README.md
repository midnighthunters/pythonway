# Q0029 · KV cache incremental decoding

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference | Hard |

## Question

Show why a KV cache is valid: implement incremental single-head causal attention that appends each new token's K and V to a cache, and verify it matches full recomputation.

## Answer

During decoding, keys and values for earlier positions never change (causal masking), so you compute K and V once per token and reuse them. Without a cache, generating n tokens costs O(n²) projections. With it, each step projects only the new token.

```python
import numpy as np


def softmax(x):
    z = x - x.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def full_causal_attention(x, wq, wk, wv):
    q, k, v = x @ wq, x @ wk, x @ wv
    n, d = q.shape
    s = q @ k.T / np.sqrt(d)
    s = np.where(np.tril(np.ones((n, n), bool)), s, -1e9)
    return softmax(s) @ v


class KVCache:
    def __init__(self, wq, wk, wv):
        self.wq, self.wk, self.wv = wq, wk, wv
        self.k: list[np.ndarray] = []
        self.v: list[np.ndarray] = []

    def step(self, x_t: np.ndarray) -> np.ndarray:
        q = x_t @ self.wq
        self.k.append(x_t @ self.wk)
        self.v.append(x_t @ self.wv)
        k, v = np.stack(self.k), np.stack(self.v)
        w = softmax(q @ k.T / np.sqrt(q.shape[-1]))
        return w @ v


rng = np.random.default_rng(0)
d = 8
x = rng.normal(size=(6, d))
wq, wk, wv = (rng.normal(size=(d, d)) for _ in range(3))
full = full_causal_attention(x, wq, wk, wv)
cache = KVCache(wq, wk, wv)
incremental = np.stack([cache.step(x[t]) for t in range(len(x))])
assert np.allclose(full, incremental)
assert len(cache.k) == 6
```

Trade-off: the cache turns compute into memory. It is often the main limit on how many concurrent requests a GPU can serve.

## Likely follow-ups

- Why can't you cache the queries?
- What happens to the KV cache when a conversation is edited in the middle?

---

[← Q0028](../../batch_01_llm_fundamentals/0028_context_window_limits_and_lost_in_the_middle/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0030 →](../../batch_01_llm_fundamentals/0030_size_the_kv_cache/README.md)

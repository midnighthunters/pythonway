# Q0031 · MQA and GQA

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Architectures | Medium |

## Question

Explain multi-query attention (MQA) and grouped-query attention (GQA), and implement the key-value head sharing in NumPy.

## Answer

- MHA: every query head has its own K and V heads.
- MQA: all query heads share one K/V head. This gives the smallest KV cache, with some quality loss.
- GQA: query heads are split into G groups, and each group shares a K/V head. It gets close to MHA quality with a much smaller cache, which makes it the common modern choice.

```python
import numpy as np


def softmax(x):
    z = x - x.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def grouped_query_attention(q, k, v):
    """q: (hq, n, d); k, v: (hkv, n, d) with hq % hkv == 0."""
    hq, hkv = q.shape[0], k.shape[0]
    if hq % hkv:
        raise ValueError("query heads must be a multiple of kv heads")
    rep = hq // hkv
    k = np.repeat(k, rep, axis=0)
    v = np.repeat(v, rep, axis=0)
    s = q @ k.transpose(0, 2, 1) / np.sqrt(q.shape[-1])
    return softmax(s) @ v


rng = np.random.default_rng(0)
q = rng.normal(size=(8, 5, 4))
k1, v1 = rng.normal(size=(1, 5, 4)), rng.normal(size=(1, 5, 4))
out = grouped_query_attention(q, k1, v1)
assert out.shape == (8, 5, 4)
k8, v8 = np.repeat(k1, 8, 0), np.repeat(v1, 8, 0)
assert np.allclose(out, grouped_query_attention(q, k8, v8))
```

The last check shows MQA is just GQA with one group. Real kernels don't materialise the repeated heads. They index into the shared head.

## Likely follow-ups

- Why does GQA mostly affect inference cost rather than training cost?

---

[← Q0030](../../batch_01_llm_fundamentals/0030_size_the_kv_cache/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0032 →](../../batch_01_llm_fundamentals/0032_prefill_versus_decode_latency/README.md)

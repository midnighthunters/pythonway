# Q0015 · LayerNorm versus RMSNorm

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Medium |

## Question

Implement LayerNorm and RMSNorm. Why have many modern LLMs switched to RMSNorm and pre-normalisation?

## Answer

```python
import numpy as np


def layer_norm(x, gamma, beta, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = x.var(-1, keepdims=True)
    return gamma * (x - mu) / np.sqrt(var + eps) + beta


def rms_norm(x, gamma, eps=1e-6):
    rms = np.sqrt((x ** 2).mean(-1, keepdims=True) + eps)
    return gamma * x / rms


rng = np.random.default_rng(0)
x = rng.normal(loc=3.0, scale=5.0, size=(4, 64))
g, b = np.ones(64), np.zeros(64)
ln = layer_norm(x, g, b)
assert np.allclose(ln.mean(-1), 0, atol=1e-6) and np.allclose(ln.std(-1), 1, atol=1e-3)
rn = rms_norm(x, g)
assert np.allclose(np.sqrt((rn ** 2).mean(-1)), 1, atol=1e-3)
assert not np.allclose(rn.mean(-1), 0, atol=1e-2)
```

- RMSNorm skips mean-centring and the bias. It is cheaper, and in practice just as effective.
- Pre-norm (normalise before each sublayer, `x + f(norm(x))`) keeps the residual stream clean and trains more stably in deep stacks than the original post-norm layout.

## Likely follow-ups

- Why is the residual connection essential for training 80+ layer models?

---

[← Q0014](../../batch_01_llm_fundamentals/0014_rotary_position_embeddings/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0016 →](../../batch_01_llm_fundamentals/0016_anatomy_of_a_decoder_block/README.md)

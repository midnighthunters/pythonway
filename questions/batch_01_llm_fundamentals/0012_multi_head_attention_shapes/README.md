# Q0012 · Multi-head attention shapes

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Medium |

## Question

Implement multi-head self-attention in NumPy: project the input to Q, K and V, split into h heads, attend per head, concatenate and project back. Verify the shapes.

## Answer

```python
import numpy as np


def softmax(x):
    z = x - x.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def multi_head_attention(x, w_q, w_k, w_v, w_o, num_heads: int, causal: bool = True):
    n, d_model = x.shape
    d_head = d_model // num_heads

    def split(t):  # (n, d_model) -> (heads, n, d_head)
        return t.reshape(n, num_heads, d_head).transpose(1, 0, 2)

    q, k, v = split(x @ w_q), split(x @ w_k), split(x @ w_v)
    scores = q @ k.transpose(0, 2, 1) / np.sqrt(d_head)
    if causal:
        scores = np.where(np.tril(np.ones((n, n), bool)), scores, -1e9)
    heads = softmax(scores) @ v
    concat = heads.transpose(1, 0, 2).reshape(n, d_model)
    return concat @ w_o


rng = np.random.default_rng(1)
n, d_model, h = 5, 16, 4
x = rng.normal(size=(n, d_model))
w = [rng.normal(size=(d_model, d_model)) * 0.1 for _ in range(4)]
out = multi_head_attention(x, *w, num_heads=h)
assert out.shape == (n, d_model)
out_prefix = multi_head_attention(x[:3], *w, num_heads=h)
assert np.allclose(out[:3], out_prefix)
```

The last assertion checks causality: outputs for the first 3 tokens don't change when later tokens are added. That property is exactly what makes KV caching valid.

Why multiple heads: each head can attend to different relations (syntax, coreference, position) in a lower-dimensional subspace at the same total cost.

## Likely follow-ups

- What are MQA and GQA, and why do they matter for inference?
- Why must `d_model` be divisible by the number of heads?

---

[← Q0011](../../batch_01_llm_fundamentals/0011_build_a_causal_attention_mask/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0013 →](../../batch_01_llm_fundamentals/0013_sinusoidal_positional_encoding/README.md)

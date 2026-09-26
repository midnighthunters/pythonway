# Q0013 · Sinusoidal positional encoding

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Easy |

## Question

Attention is permutation-invariant. Implement the original sinusoidal positional encoding and explain why position information is needed.

## Answer

Without positional information, "dog bites man" and "man bites dog" produce the same attention outputs up to permutation. The original Transformer adds `PE[pos, 2i] = sin(pos / 10000^(2i/d))` and `PE[pos, 2i+1] = cos(...)` to the embeddings.

```python
import numpy as np


def sinusoidal_positions(n: int, d: int) -> np.ndarray:
    pos = np.arange(n)[:, None]
    i = np.arange(0, d, 2)[None, :]
    angles = pos / np.power(10000.0, i / d)
    pe = np.zeros((n, d))
    pe[:, 0::2] = np.sin(angles)
    pe[:, 1::2] = np.cos(angles)
    return pe


pe = sinusoidal_positions(50, 16)
assert pe.shape == (50, 16)
assert np.allclose(pe[0, 0::2], 0) and np.allclose(pe[0, 1::2], 1)
assert np.all(np.abs(pe) <= 1)
assert len({tuple(np.round(r, 6)) for r in pe}) == 50
```

Modern LLMs mostly use RoPE (rotary embeddings) instead, which encode relative position directly in the Q·K product and extend to longer contexts with scaling tricks.

## Likely follow-ups

- What is the difference between absolute, relative and rotary position encodings?
- How do models extend their context window after training (RoPE scaling, YaRN)?

---

[← Q0012](../../batch_01_llm_fundamentals/0012_multi_head_attention_shapes/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0014 →](../../batch_01_llm_fundamentals/0014_rotary_position_embeddings/README.md)

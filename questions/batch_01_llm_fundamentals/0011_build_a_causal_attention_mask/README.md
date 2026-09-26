# Q0011 · Build a causal attention mask

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Transformers | Easy |

## Question

Build the causal (look-ahead) mask for a decoder with sequence length n, and combine it with a padding mask for a batch of right-padded sequences.

## Answer

```python
import numpy as np


def causal_mask(n: int) -> np.ndarray:
    return np.tril(np.ones((n, n), dtype=bool))


def combined_mask(lengths: list[int], n: int) -> np.ndarray:
    """Shape (batch, n, n). True = query i may attend to key j."""
    key_valid = np.arange(n)[None, :] < np.array(lengths)[:, None]
    return causal_mask(n)[None, :, :] & key_valid[:, None, :]


m = causal_mask(3)
assert m.tolist() == [[True, False, False], [True, True, False], [True, True, True]]
cm = combined_mask([2, 3], 3)
assert cm.shape == (2, 3, 3)
assert not cm[0, 2, 2] and cm[0, 2, 1] and cm[1, 2, 2]
```

Why: during training all positions are processed in parallel, and the mask stops position i from seeing future tokens, so training matches left-to-right generation. Padding masks stop real tokens from attending to pad tokens.

Gotcha: with left padding (common in batched generation), the mask and position ids must be offset. Mismatched padding side is a classic source of garbage batched output.

## Likely follow-ups

- Why do inference servers prefer left padding for batched generation?
- What is a sliding-window mask, and which models use it?

---

[← Q0010](../../batch_01_llm_fundamentals/0010_why_attention_scales_by_the_square_root_of_d_k/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0012 →](../../batch_01_llm_fundamentals/0012_multi_head_attention_shapes/README.md)

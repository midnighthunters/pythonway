# Q0077 · Sliding-window attention mask

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Long context | Medium |

## Question

Implement a causal sliding-window attention mask of width w, and explain how stacking layers still lets information travel further than w.

## Answer

Each token attends only to itself and the previous w-1 tokens, so attention cost is O(n·w) instead of O(n²), and the KV cache per layer is capped at w tokens. With L layers, the receptive field grows to about L × w, because information hops forward one window per layer. Some models mix sliding-window layers with a few global-attention layers.

```python
import numpy as np


def sliding_window_mask(n: int, w: int) -> np.ndarray:
    i = np.arange(n)[:, None]
    j = np.arange(n)[None, :]
    return (j <= i) & (i - j < w)


m = sliding_window_mask(5, 2)
assert m[4].tolist() == [False, False, False, True, True]
assert m.sum() == 9
assert np.array_equal(sliding_window_mask(6, 6), np.tril(np.ones((6, 6), bool)))
```

## Likely follow-ups

- What does a sliding window do to the KV-cache memory for a 128k-token conversation?

---

[← Q0076](../../batch_01_llm_fundamentals/0076_why_llms_struggle_with_character_level_tasks/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0078 →](../../batch_01_llm_fundamentals/0078_alternatives_to_quadratic_attention/README.md)

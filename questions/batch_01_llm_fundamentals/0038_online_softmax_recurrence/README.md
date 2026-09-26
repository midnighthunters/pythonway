# Q0038 · Online softmax recurrence

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference performance | Hard |

## Question

Implement the online (streaming) softmax used by FlashAttention: process scores in blocks, keep a running max `m` and denominator `l`, and accumulate the weighted sum of value vectors. Verify it against standard softmax attention.

## Answer

When a new block raises the maximum from `m` to `m'`, rescale the previous accumulators by `exp(m - m')`.

```python
import numpy as np


def streaming_attention_row(scores: np.ndarray, values: np.ndarray, block: int) -> np.ndarray:
    m, l = -np.inf, 0.0
    acc = np.zeros(values.shape[1])
    for start in range(0, len(scores), block):
        s = scores[start:start + block]
        v = values[start:start + block]
        m_new = max(m, float(s.max()))
        correction = np.exp(m - m_new) if np.isfinite(m) else 0.0
        p = np.exp(s - m_new)
        l = l * correction + p.sum()
        acc = acc * correction + p @ v
        m = m_new
    return acc / l


rng = np.random.default_rng(0)
scores = rng.normal(size=37) * 5
values = rng.normal(size=(37, 4))
w = np.exp(scores - scores.max())
reference = (w / w.sum()) @ values
for block in (1, 4, 8, 37, 64):
    assert np.allclose(streaming_attention_row(scores, values, block), reference)
```

This recurrence is why attention can be computed in one pass over K and V blocks with constant extra memory per query row.

## Likely follow-ups

- How does the same trick let you combine attention results computed on different GPUs (ring attention, context parallelism)?

---

[← Q0037](../../batch_01_llm_fundamentals/0037_flashattention_in_one_answer/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0039 →](../../batch_01_llm_fundamentals/0039_pagedattention_and_vllm/README.md)

# Q0084 · FP16 versus BF16 overflow

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Numerics | Medium |

## Question

Show numerically why BF16 is preferred over FP16 for training and many inference paths, by simulating BF16 rounding from float32 and comparing range and precision.

## Answer

FP16 has 5 exponent bits (maximum about 65,504) and 10 mantissa bits. BF16 has 8 exponent bits (the same range as FP32) and only 7 mantissa bits. BF16 rarely overflows, so no loss scaling is needed, but it is less precise.

```python
import warnings

import numpy as np


def to_bf16(x) -> np.ndarray:
    a = np.asarray(x, dtype=np.float32)
    bits = a.view(np.uint32).astype(np.uint64)
    rounded = ((bits + 0x7FFF + ((bits >> 16) & 1)) & 0xFFFF0000).astype(np.uint32)
    return rounded.view(np.float32)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    assert np.isinf(np.array([70000.0]).astype(np.float16)[0])
bf = float(to_bf16(70000.0))
assert np.isfinite(bf) and abs(bf - 70000) / 70000 < 0.01
assert float(to_bf16(1.001)) == 1.0
assert float(np.float16(1.001)) != 1.0
```

70,000 overflows FP16 to infinity but is fine in BF16. 1.001 keeps its fraction in FP16 but rounds to 1.0 in BF16.

Takeaways: activations and logits can exceed the FP16 range (for example after an `exp`), producing inf and NaN. BF16 avoids that at the cost of precision, which is why softmax and normalisation accumulations are often kept in FP32 inside kernels.

## Likely follow-ups

- What is loss scaling, and why does FP16 training need it?

---

[← Q0083](../../batch_01_llm_fundamentals/0083_logit_bias_to_ban_or_force_tokens/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0085 →](../../batch_01_llm_fundamentals/0085_agent_latency_budget_with_parallel_stages/README.md)

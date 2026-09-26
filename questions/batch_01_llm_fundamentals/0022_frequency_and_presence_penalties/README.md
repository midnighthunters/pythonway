# Q0022 · Frequency and presence penalties

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding | Medium |

## Question

Implement OpenAI-style frequency and presence penalties on logits, given the tokens generated so far. How do they differ from a repetition penalty?

## Answer

Frequency penalty subtracts `α × count(token)`, and presence penalty subtracts `β × [count > 0]`. Both lower the chance of reusing tokens, discouraging loops and repeated phrases.

```python
from collections import Counter

import numpy as np


def apply_penalties(logits: np.ndarray, generated: list[int], frequency: float = 0.0,
                    presence: float = 0.0) -> np.ndarray:
    out = logits.astype(float).copy()
    for tok, count in Counter(generated).items():
        out[tok] -= frequency * count + presence
    return out


logits = np.zeros(4)
adj = apply_penalties(logits, [1, 1, 1, 2], frequency=0.5, presence=1.0)
assert adj.tolist() == [0.0, -2.5, -1.5, 0.0]
assert apply_penalties(logits, [3], 0.0, 0.0).tolist() == [0.0] * 4
```

The Hugging Face-style `repetition_penalty` is multiplicative instead: it divides positive logits and multiplies negative logits of previously seen tokens by the factor.

Caution: penalties also discourage legitimately repeated tokens, such as JSON keys, code identifiers and numbers. Keep them at 0 for structured output and code.

## Likely follow-ups

- Why can a presence penalty break JSON generation?

---

[← Q0021](../../batch_01_llm_fundamentals/0021_top_p_nucleus_sampling/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0023 →](../../batch_01_llm_fundamentals/0023_beam_search/README.md)

# Q0019 · Temperature scaling

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding | Easy |

## Question

Implement temperature sampling and show how temperature changes the distribution's entropy. What does temperature 0 mean in practice?

## Answer

Divide the logits by T before softmax. T < 1 sharpens the distribution (lower entropy), and T > 1 flattens it. T → 0 approaches greedy argmax, so implementations special-case T = 0 to argmax rather than dividing by zero.

```python
import numpy as np


def softmax(x):
    z = x - x.max()
    e = np.exp(z)
    return e / e.sum()


def entropy(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def sample_with_temperature(logits: np.ndarray, t: float, rng: np.random.Generator) -> int:
    if t < 0:
        raise ValueError("temperature must be >= 0")
    if t == 0:
        return int(np.argmax(logits))
    return int(rng.choice(len(logits), p=softmax(logits / t)))


logits = np.array([2.0, 1.0, 0.5, -1.0])
h_low, h_mid, h_high = (entropy(softmax(logits / t)) for t in (0.3, 1.0, 2.0))
assert h_low < h_mid < h_high
rng = np.random.default_rng(0)
assert sample_with_temperature(logits, 0, rng) == 0
draws = [sample_with_temperature(logits, 1.0, rng) for _ in range(2000)]
assert 0.55 < draws.count(0) / 2000 < 0.70
```

Guidance: use low temperature for extraction, classification, tool calls and code. Use moderate temperature for drafting and brainstorming. Tune either temperature or top-p, not both aggressively. Some reasoning models fix or ignore sampling parameters, so check the provider docs.

## Likely follow-ups

- Why is temperature 0 still not fully deterministic on hosted APIs?
- What temperature would you set for a compliance summary, and why?

---

[← Q0018](../../batch_01_llm_fundamentals/0018_greedy_decoding_loop/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0020 →](../../batch_01_llm_fundamentals/0020_top_k_sampling/README.md)

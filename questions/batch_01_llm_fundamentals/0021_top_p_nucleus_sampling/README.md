# Q0021 · Top-p nucleus sampling

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding | Medium |

## Question

Implement nucleus (top-p) sampling: keep the smallest set of most-probable tokens whose cumulative probability reaches p, renormalise and sample.

## Answer

```python
import numpy as np


def softmax(x):
    z = x - x.max()
    e = np.exp(z)
    return e / e.sum()


def top_p_probs(logits: np.ndarray, p: float) -> np.ndarray:
    if not 0 < p <= 1:
        raise ValueError("p must be in (0, 1]")
    probs = softmax(logits)
    order = np.argsort(-probs, kind="stable")
    cum = np.cumsum(probs[order])
    cutoff = int(np.searchsorted(cum, p)) + 1
    keep = order[:cutoff]
    out = np.zeros_like(probs)
    out[keep] = probs[keep]
    return out / out.sum()


logits = np.log(np.array([0.5, 0.3, 0.15, 0.05]))
assert np.allclose(top_p_probs(logits, 0.75), [0.625, 0.375, 0, 0])
assert np.allclose(top_p_probs(logits, 0.85), [0.5 / 0.95, 0.3 / 0.95, 0.15 / 0.95, 0])
assert np.allclose(top_p_probs(logits, 1.0), [0.5, 0.3, 0.15, 0.05])
assert np.allclose(top_p_probs(logits, 0.1), [1, 0, 0, 0])
rng = np.random.default_rng(0)
assert rng.choice(4, p=top_p_probs(logits, 0.75)) in (0, 1)
```

`searchsorted` finds the first index where the cumulative sum reaches p. The +1 includes the token that crosses the threshold, so at least one token is always kept.

Testing pitfall: don't test exactly at a boundary such as p = 0.8 here. The float cumulative sum may be 0.8000000000000002, which flips the result. That is a good example of a flaky test to mention in an interview.

Related: min-p sampling keeps tokens with probability ≥ `min_p × max_prob`, which scales naturally with the model's confidence.

## Likely follow-ups

- Why is top-p usually preferred over top-k for chat models?

---

[← Q0020](../../batch_01_llm_fundamentals/0020_top_k_sampling/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0022 →](../../batch_01_llm_fundamentals/0022_frequency_and_presence_penalties/README.md)

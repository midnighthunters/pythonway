# Q0026 · Next-token cross-entropy loss

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Training | Medium |

## Question

Implement the next-token cross-entropy loss for a batch of logits `(batch, seq, vocab)` and targets `(batch, seq)`, ignoring padding positions marked `-100`.

## Answer

The inputs are shifted by one: position t predicts token t+1. The loss is the mean negative log-probability of the correct next token over non-ignored positions. Using `-100` as the ignore index is the PyTorch and Hugging Face convention, and it is also how SFT masks prompt tokens so only the response is trained on.

```python
import numpy as np


def log_softmax(x):
    z = x - x.max(-1, keepdims=True)
    return z - np.log(np.exp(z).sum(-1, keepdims=True))


def causal_lm_loss(logits: np.ndarray, targets: np.ndarray, ignore_index: int = -100) -> float:
    lp = log_softmax(logits)
    mask = targets != ignore_index
    safe = np.where(mask, targets, 0)
    picked = np.take_along_axis(lp, safe[..., None], axis=-1)[..., 0]
    return float(-(picked * mask).sum() / mask.sum())


vocab = 4
logits = np.zeros((1, 3, vocab))
assert np.isclose(causal_lm_loss(logits, np.array([[1, 2, 3]])), np.log(4))
confident = np.full((1, 2, vocab), -20.0)
confident[0, 0, 2] = confident[0, 1, 3] = 20.0
assert causal_lm_loss(confident, np.array([[2, 3]])) < 1e-6
assert np.isclose(causal_lm_loss(logits, np.array([[1, -100, -100]])), np.log(4))
```

Sanity check worth knowing: at initialisation the loss should be about `ln(vocab_size)`, which is roughly 11.9 for a 150k vocabulary. A very different number means a bug.

## Likely follow-ups

- Why mask the prompt tokens during supervised fine-tuning?
- How does label smoothing change this loss?

---

[← Q0025](../../batch_01_llm_fundamentals/0025_sequence_log_probability_and_perplexity/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0027 →](../../batch_01_llm_fundamentals/0027_why_llms_hallucinate/README.md)

# Q0083 · Logit bias to ban or force tokens

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding controls | Easy |

## Question

Implement a logit-bias function (token id to bias in [-100, 100], where -100 effectively bans the token) and show how it changes the chosen token. What are the practical uses and pitfalls?

## Answer

```python
import numpy as np


def apply_logit_bias(logits: np.ndarray, bias: dict[int, float]) -> np.ndarray:
    out = logits.astype(float).copy()
    for tok, b in bias.items():
        if not -100 <= b <= 100:
            raise ValueError("bias must be within [-100, 100]")
        out[tok] = -np.inf if b == -100 else out[tok] + b
    return out


logits = np.array([2.0, 1.5, 0.1])
assert int(np.argmax(apply_logit_bias(logits, {0: -100}))) == 1
assert int(np.argmax(apply_logit_bias(logits, {2: 5}))) == 2
assert np.isneginf(apply_logit_bias(logits, {1: -100})[1])
```

Uses: restrict a classifier to label tokens, ban a known-bad token, discourage a phrase.

Pitfalls: biases apply to token ids, which are tokenizer-specific, and a word may span several tokens with different ids for " word" and "word". Support varies by provider and model, and many reasoning models don't support it. Structured outputs or enums are usually a more robust way to constrain answers.

## Likely follow-ups

- Why is banning a word by token id fragile?

---

[← Q0082](../../batch_01_llm_fundamentals/0082_expected_calibration_error/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0084 →](../../batch_01_llm_fundamentals/0084_fp16_versus_bf16_overflow/README.md)

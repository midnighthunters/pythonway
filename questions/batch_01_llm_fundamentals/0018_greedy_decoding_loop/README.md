# Q0018 · Greedy decoding loop

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding | Easy |

## Question

Implement a greedy decoding loop over a model function `next_logits(tokens) -> np.ndarray`, stopping at an end-of-sequence id or `max_new_tokens`. Return the tokens and the finish reason.

## Answer

```python
import numpy as np

EOS = 0


def greedy_decode(next_logits, prompt: list[int], max_new_tokens: int) -> tuple[list[int], str]:
    tokens = list(prompt)
    for _ in range(max_new_tokens):
        nxt = int(np.argmax(next_logits(tokens)))
        if nxt == EOS:
            return tokens[len(prompt):], "stop"
        tokens.append(nxt)
    return tokens[len(prompt):], "length"


def fake_model(tokens: list[int]) -> np.ndarray:
    logits = np.full(6, -5.0)
    nxt = tokens[-1] + 1 if tokens[-1] < 4 else EOS
    logits[nxt] = 5.0
    return logits


assert greedy_decode(fake_model, [1], 10) == ([2, 3, 4], "stop")
assert greedy_decode(fake_model, [1], 2) == ([2, 3], "length")
```

The finish reason matters in production. APIs return `finish_reason` / `stop_reason` values such as `stop`, `length`, `tool_calls` and `content_filter`, and callers must handle `length` (truncated output, for example broken JSON) differently from `stop`.

Greedy decoding is deterministic in theory but can loop and repeat, and it isn't always the highest-probability sequence overall.

## Likely follow-ups

- Why can greedy decoding miss the most likely full sequence?
- How should a client react to `finish_reason == "length"` when it expected JSON?

---

[← Q0017](../../batch_01_llm_fundamentals/0017_encoder_decoder_and_encoder_decoder_models/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0019 →](../../batch_01_llm_fundamentals/0019_temperature_scaling/README.md)

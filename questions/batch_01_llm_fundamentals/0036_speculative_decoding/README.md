# Q0036 · Speculative decoding

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Inference performance | Hard |

## Question

Explain speculative decoding and why its output distribution matches the target model exactly. Then simulate the expected number of tokens accepted per step.

## Answer

- A small draft model proposes k tokens cheaply. The large target model scores all k in one parallel forward pass.
- Each drafted token is accepted with probability `min(1, p_target / p_draft)`. At the first rejection, the target samples a replacement from the normalised residual `max(0, p_target - p_draft)`. This rejection-sampling scheme makes the output distribution identical to sampling from the target alone.
- Speed-up comes from turning several sequential target decode steps into one verification step. It works best when the draft agrees often (predictable text, code).

If each token is accepted independently with probability α, the expected tokens per target pass are `(1 - α^(k+1)) / (1 - α)`, counting the bonus token.

```python
import random


def expected_tokens_per_step(alpha: float, k: int) -> float:
    return (1 - alpha ** (k + 1)) / (1 - alpha) if alpha < 1 else k + 1


def simulate(alpha: float, k: int, trials: int = 200_000, seed: int = 0) -> float:
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        accepted = 0
        while accepted < k and rng.random() < alpha:
            accepted += 1
        total += accepted + 1
    return total / trials


for alpha, k in ((0.8, 4), (0.5, 3), (0.95, 8)):
    assert abs(simulate(alpha, k) - expected_tokens_per_step(alpha, k)) < 0.02
assert round(expected_tokens_per_step(0.8, 4), 2) == 3.36
```

Variants include Medusa and EAGLE (extra draft heads on the target itself) and prompt-lookup decoding, which drafts by copying n-grams from the prompt and is great for RAG and code editing.

## Likely follow-ups

- Why does speculative decoding help less at large batch sizes?

---

[← Q0035](../../batch_01_llm_fundamentals/0035_symmetric_int8_quantization/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0037 →](../../batch_01_llm_fundamentals/0037_flashattention_in_one_answer/README.md)

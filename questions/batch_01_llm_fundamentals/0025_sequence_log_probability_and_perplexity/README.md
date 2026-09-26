# Q0025 · Sequence log-probability and perplexity

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Evaluation math | Medium |

## Question

Given per-token log-probabilities for a sequence, compute its total log-probability, average negative log-likelihood and perplexity. What does perplexity tell you and not tell you?

## Answer

Perplexity is `exp(mean NLL)`, the effective number of equally likely choices per token. Lower means the model finds the text more predictable.

```python
import math


def sequence_stats(token_logprobs: list[float]) -> dict[str, float]:
    if not token_logprobs:
        raise ValueError("empty sequence")
    total = sum(token_logprobs)
    nll = -total / len(token_logprobs)
    return {"logprob": total, "avg_nll": nll, "perplexity": math.exp(nll)}


uniform4 = [math.log(0.25)] * 10
assert math.isclose(sequence_stats(uniform4)["perplexity"], 4.0)
certain = [0.0] * 5
assert sequence_stats(certain)["perplexity"] == 1.0
mixed = sequence_stats([math.log(0.5), math.log(0.125)])
assert math.isclose(mixed["perplexity"], 4.0)
```

What it tells you: fit to a distribution, which is useful for comparing language models on the same tokenizer and dataset, for spotting out-of-domain or garbled text, and for detecting some training-data memorisation.

What it doesn't tell you: helpfulness, factual correctness or instruction following. It isn't comparable across different tokenizers. Task-level evaluations matter far more for an assistant platform.

## Likely follow-ups

- Why can't you compare perplexity between two models with different tokenizers?
- How is perplexity used in some AI-text detectors, and why are they unreliable?

---

[← Q0024](../../batch_01_llm_fundamentals/0024_log_probabilities_as_confidence_signals/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0026 →](../../batch_01_llm_fundamentals/0026_next_token_cross_entropy_loss/README.md)

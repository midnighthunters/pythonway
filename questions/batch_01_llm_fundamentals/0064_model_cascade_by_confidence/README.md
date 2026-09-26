# Q0064 · Model cascade by confidence

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Model routing | Medium |

## Question

Implement a model cascade: try a cheap model first and escalate to larger models only when confidence is below a threshold. Return the answer, the model used and the total cost.

## Answer

Why it matters here: on a platform serving hundreds of thousands of users, most requests are easy. Cascades cut cost while keeping hard cases on strong models.

```python
from typing import Callable

Model = Callable[[str], tuple[str, float]]


def cascade(prompt: str, tiers: list[tuple[str, Model, int]], threshold: float) -> dict:
    spent = 0
    for i, (name, model, cost) in enumerate(tiers):
        answer, conf = model(prompt)
        spent += cost
        if conf >= threshold or i == len(tiers) - 1:
            return {"model": name, "answer": answer, "confidence": conf, "cost_micro_usd": spent}
    raise ValueError("no tiers configured")


def small(prompt: str) -> tuple[str, float]:
    return ("small-answer", 0.9 if "easy" in prompt else 0.4)


def large(prompt: str) -> tuple[str, float]:
    return ("large-answer", 0.95)


tiers = [("small", small, 50), ("large", large, 1_000)]
assert cascade("easy question", tiers, 0.8) == {"model": "small", "answer": "small-answer",
                                                 "confidence": 0.9, "cost_micro_usd": 50}
hard = cascade("hard question", tiers, 0.8)
assert hard["model"] == "large" and hard["cost_micro_usd"] == 1_050
```

The confidence signal is the hard part. Options include logprobs, a verifier model, self-reported confidence (weak), rule checks such as schema validity or citations present, or a trained router that predicts difficulty up front and avoids paying for both calls.

## Likely follow-ups

- When is a router (predict first) better than a cascade (try, then escalate)?

---

[← Q0063](../../batch_01_llm_fundamentals/0063_estimate_image_token_cost/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0065 →](../../batch_01_llm_fundamentals/0065_choosing_a_model_for_a_use_case/README.md)

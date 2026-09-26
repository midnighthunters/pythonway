# Q0309 · Semantic similarity scoring and its limits

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Metrics | Medium |

## Question

Scoring answers by embedding similarity to a reference is popular. Show with a toy example why it fails on negation, and state when it's still useful.

## Answer

```python
import math
import re
from collections import Counter


def embed(text: str) -> Counter:
    return Counter(re.findall(r"[a-z]+", text.lower()))


def cosine(a: Counter, b: Counter) -> float:
    dot = sum(a[t] * b[t] for t in a)
    return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())))


ref = "The expense claim was approved by finance on Monday"
assert cosine(embed(ref), embed("The expense claim was not approved by finance on Monday")) > 0.9
assert cosine(embed(ref), embed("Finance approved it")) < 0.5
```

The wrong answer scores 0.95 and the correct terse answer scores low. Real embedding models behave better than bag-of-words, but have the same blind spots: negation, numbers and entity swaps.

Still useful for: clustering outputs, detecting drift, semantic cache hits (with strict thresholds), finding near-duplicate evaluation cases, and as a coarse signal alongside precise checks. Don't use it as the accuracy metric for facts.

## Likely follow-ups

- What would you combine with similarity to make it safer as a metric?

---

[← Q0308](../../batch_04_llm_evaluation_observability/0308_why_bleu_and_rouge_mislead_for_llm_outputs/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0310 →](../../batch_04_llm_evaluation_observability/0310_precision_recall_and_f1_per_label/README.md)

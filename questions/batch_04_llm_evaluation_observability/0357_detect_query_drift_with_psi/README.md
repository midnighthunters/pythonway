# Q0357 · Detect query drift with PSI

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Monitoring | Medium |

## Question

Implement the population stability index (PSI) over categorical query intents to detect when the production mix drifts away from the evaluation set's distribution.

## Answer

```python
import math
from collections import Counter


def psi(expected: list[str], actual: list[str], eps: float = 1e-4) -> float:
    cats = set(expected) | set(actual)
    e, a = Counter(expected), Counter(actual)
    total = 0.0
    for c in cats:
        pe = max(e[c] / len(expected), eps)
        pa = max(a[c] / len(actual), eps)
        total += (pa - pe) * math.log(pa / pe)
    return total


baseline = ["policy"] * 60 + ["it"] * 30 + ["hr"] * 10
same = ["policy"] * 58 + ["it"] * 31 + ["hr"] * 11
shifted = ["policy"] * 30 + ["it"] * 20 + ["hr"] * 10 + ["sanctions"] * 40
assert psi(baseline, same) < 0.01
assert psi(baseline, shifted) > 0.25
```

Common rule of thumb: below 0.1 is stable, 0.1–0.25 is a moderate shift, and above 0.25 is a significant shift. A new "sanctions" intent at 40% means the evaluation set no longer represents production: add cases for it, and check that the assistant handles it. Compute intents with a cheap classifier over sampled queries.

## Likely follow-ups

- What does a PSI alert tell you, and what doesn't it tell you?

---

[← Q0356](../../batch_04_llm_evaluation_observability/0356_implicit_feedback_signals/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0358 →](../../batch_04_llm_evaluation_observability/0358_detect_embedding_drift/README.md)

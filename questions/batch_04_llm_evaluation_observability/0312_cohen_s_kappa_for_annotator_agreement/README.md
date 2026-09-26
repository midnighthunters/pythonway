# Q0312 · Cohen's kappa for annotator agreement

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Human evaluation | Medium |

## Question

Two SMEs labelled the same answers as correct or incorrect. Implement Cohen's kappa and explain why raw agreement isn't enough.

## Answer

```python
from collections import Counter


def cohens_kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in ca.keys() | cb.keys()) / n ** 2
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


a = ["y", "y", "n", "n", "y", "n"]
b = ["y", "n", "n", "n", "y", "y"]
assert abs(cohens_kappa(a, b) - 1 / 3) < 1e-12
assert cohens_kappa(a, a) == 1.0
skewed_a, skewed_b = ["y"] * 18 + ["n", "y"], ["y"] * 18 + ["y", "n"]
assert sum(x == y for x, y in zip(skewed_a, skewed_b)) / 20 == 0.9 and cohens_kappa(skewed_a, skewed_b) < 0
```

Kappa corrects for chance agreement. In the skewed example, the annotators agree 90% of the time just by both saying "yes", yet kappa is negative. Rough guide: above 0.6 is substantial, above 0.8 is strong. Low agreement means your rubric or guidelines are unclear. Fix them before trusting any metric built on these labels, including LLM-judge calibration.

## Likely follow-ups

- What would you do when two domain experts genuinely disagree?

---

[← Q0311](../../batch_04_llm_evaluation_observability/0311_confusion_matrix_for_intent_routing/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0313 →](../../batch_04_llm_evaluation_observability/0313_bootstrap_confidence_intervals_for_a_metric/README.md)

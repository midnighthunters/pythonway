# Q0313 · Bootstrap confidence intervals for a metric

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Statistics | Medium |

## Question

Your new prompt scores 84% on 200 cases versus 81% before. Implement a bootstrap confidence interval for accuracy and for the paired difference, and interpret it.

## Answer

```python
import random


def bootstrap_ci(values: list[float], n_boot: int = 2_000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_boot))
    return means[int(alpha / 2 * n_boot)], means[int((1 - alpha / 2) * n_boot) - 1]


def paired_diff_ci(a: list[int], b: list[int], **kw) -> tuple[float, float]:
    return bootstrap_ci([y - x for x, y in zip(a, b)], **kw)


rng = random.Random(42)
old = [1 if rng.random() < 0.81 else 0 for _ in range(200)]
new = [o if rng.random() < 0.9 else 1 for o in old]
lo, hi = bootstrap_ci(new)
assert lo < sum(new) / len(new) < hi and hi - lo < 0.15
dlo, dhi = paired_diff_ci(old, new)
assert dlo >= 0 and dhi > 0
```

Resampling cases with replacement shows how much the metric would move with a different sample of 200 cases. For comparing versions, bootstrap the paired per-case difference: it is much tighter than comparing two independent intervals, because both versions saw the same cases. If the interval for the difference includes 0, you haven't shown an improvement. Get more cases or repeat runs.

## Likely follow-ups

- Why is the paired interval narrower than the difference of two separate intervals?

---

[← Q0312](../../batch_04_llm_evaluation_observability/0312_cohen_s_kappa_for_annotator_agreement/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0314 →](../../batch_04_llm_evaluation_observability/0314_sample_size_for_detecting_an_improvement/README.md)

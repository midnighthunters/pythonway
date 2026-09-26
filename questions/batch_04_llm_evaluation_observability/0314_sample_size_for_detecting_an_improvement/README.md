# Q0314 · Sample size for detecting an improvement

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Statistics | Medium |

## Question

How many evaluation cases do you need to reliably detect an accuracy improvement from 80% to 85%? Implement the standard two-proportion sample-size formula.

## Answer

```python
import math
from statistics import NormalDist


def n_per_group(p1: float, p2: float, alpha: float = 0.05, power: float = 0.8) -> int:
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)
    p_bar = (p1 + p2) / 2
    num = (z_a * math.sqrt(2 * p_bar * (1 - p_bar)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (p1 - p2) ** 2)


n = n_per_group(0.80, 0.85)
assert 900 <= n <= 910
assert n_per_group(0.80, 0.90) < n / 3
```

About 900 cases per group for a 5-point difference with independent samples. In practice you compare two versions on the same cases, and a paired test (McNemar, or a sign test on discordant cases) needs fewer, because only the cases that flip matter. The takeaway for interviews: 50-case evaluation sets can only detect large differences. Small wins need hundreds of cases, repeated runs, or both.

## Likely follow-ups

- Why does a paired design need fewer cases?

---

[← Q0313](../../batch_04_llm_evaluation_observability/0313_bootstrap_confidence_intervals_for_a_metric/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0315 →](../../batch_04_llm_evaluation_observability/0315_unbiased_pass_k/README.md)

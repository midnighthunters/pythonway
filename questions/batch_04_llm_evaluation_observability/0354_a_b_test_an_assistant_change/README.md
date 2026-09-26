# Q0354 · A/B test an assistant change

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Online evaluation | Medium |

## Question

Variant B has a 52.0% positive-feedback rate over 1,000 rated answers, and A has 48.0% over 1,000. Implement a two-proportion z-test and interpret it. What else must you check?

## Answer

```python
import math
from statistics import NormalDist


def two_proportion_z(success_a: int, n_a: int, success_b: int, n_b: int) -> tuple[float, float]:
    pa, pb = success_a / n_a, success_b / n_b
    p = (success_a + success_b) / (n_a + n_b)
    se = math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))
    z = (pb - pa) / se
    return z, 2 * (1 - NormalDist().cdf(abs(z)))


z, p = two_proportion_z(480, 1_000, 520, 1_000)
assert 1.7 < z < 1.9 and 0.07 < p < 0.08
z2, p2 = two_proportion_z(4_800, 10_000, 5_200, 10_000)
assert p2 < 0.001
```

With p ≈ 0.07, a 4-point lift on 1,000 ratings each isn't conclusive at the usual 5% level. The same lift on 10,000 ratings would be.

Also check:
- Randomise by user, not by request, so one user's experience stays consistent and ratings stay independent.
- Selection bias: only some users rate answers. Look at implicit signals too.
- Guardrail metrics: safety, latency, cost and abstention mustn't degrade.
- Novelty effects (run long enough), and segments (languages, business lines).
- Decide the sample size and duration in advance, and don't stop when the p-value first dips below 0.05.

## Likely follow-ups

- Why does peeking at results daily inflate false positives?

---

[← Q0353](../../batch_04_llm_evaluation_observability/0353_offline_versus_online_evaluation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0355 →](../../batch_04_llm_evaluation_observability/0355_guardrail_metrics_in_production/README.md)

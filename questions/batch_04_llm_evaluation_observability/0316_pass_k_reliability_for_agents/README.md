# Q0316 · pass^k reliability for agents

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Agent metrics | Medium |

## Question

For an agent that users run once, reliability matters more than "succeeds sometimes". Implement pass^k (the probability that k independent runs all succeed) from n trials with c successes, and compare it with pass@k.

## Answer

```python
from math import comb


def pass_hat_k(n: int, c: int, k: int) -> float:
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    return comb(c, k) / comb(n, k)


def pass_at_k(n: int, c: int, k: int) -> float:
    return 1.0 if n - c < k else 1 - comb(n - c, k) / comb(n, k)


assert abs(pass_hat_k(10, 8, 3) - 56 / 120) < 1e-12
assert pass_hat_k(10, 8, 1) == 0.8
assert pass_at_k(10, 8, 3) == 1.0
```

With 80% single-run success, three-in-a-row reliability is only about 47%, while pass@3 is 100%. For customer-facing or operations agents (for example booking or remediation workflows), report pass^k or the per-run success rate with its variance. A system that works "on some runs" isn't production-ready.

## Likely follow-ups

- How would you raise pass^k without changing the model?

---

[← Q0315](../../batch_04_llm_evaluation_observability/0315_unbiased_pass_k/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0317 →](../../batch_04_llm_evaluation_observability/0317_llm_as_judge_design/README.md)

# Q0315 · Unbiased pass@k

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Code and agent metrics | Medium |

## Question

Implement the unbiased pass@k estimator used in code-generation benchmarks: from n samples with c correct, estimate the probability that at least one of k samples passes.

## Answer

pass@k = 1 - C(n-c, k) / C(n, k): one minus the probability that all k samples drawn without replacement fail.

```python
from math import comb


def pass_at_k(n: int, c: int, k: int) -> float:
    if not 0 <= c <= n or not 1 <= k <= n:
        raise ValueError("need 0 <= c <= n and 1 <= k <= n")
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


assert abs(pass_at_k(10, 3, 1) - 0.3) < 1e-12
assert pass_at_k(10, 3, 10) == 1.0
assert pass_at_k(10, 0, 5) == 0.0
assert abs(pass_at_k(10, 3, 2) - (1 - comb(7, 2) / comb(10, 2))) < 1e-12
```

The naive `1 - (1 - c/n)^k` is biased. Averaging the unbiased estimator per problem, then across problems, gives the benchmark score. pass@k measures "can it ever get it right", which is relevant when a verifier (unit tests) picks the passing sample.

## Likely follow-ups

- When is pass@k the wrong metric for a production agent?

---

[← Q0314](../../batch_04_llm_evaluation_observability/0314_sample_size_for_detecting_an_improvement/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0316 →](../../batch_04_llm_evaluation_observability/0316_pass_k_reliability_for_agents/README.md)

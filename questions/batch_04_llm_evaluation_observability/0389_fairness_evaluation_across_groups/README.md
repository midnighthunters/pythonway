# Q0389 · Fairness evaluation across groups

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Responsible AI | Medium |

## Question

An HR policy assistant is used by employees across regions and grades. Implement a parity check: compute a quality metric per group, report the largest gap, and flag it when it exceeds a tolerance (only for groups with enough samples).

## Answer

```python
from collections import defaultdict


def parity_report(results: list[dict], group_key: str, tolerance: float, min_n: int = 30) -> dict:
    agg: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for r in results:
        agg[r[group_key]][0] += r["correct"]
        agg[r[group_key]][1] += 1
    rates = {g: c / n for g, (c, n) in agg.items() if n >= min_n}
    gap = max(rates.values()) - min(rates.values()) if len(rates) > 1 else 0.0
    return {"rates": rates, "gap": gap, "flag": gap > tolerance,
            "underpowered": sorted(g for g, (_, n) in agg.items() if n < min_n)}


results = ([{"region": "UK", "correct": 1}] * 90 + [{"region": "UK", "correct": 0}] * 10
           + [{"region": "India", "correct": 1}] * 70 + [{"region": "India", "correct": 0}] * 30
           + [{"region": "Brazil", "correct": 1}] * 5)
r = parity_report(results, "region", tolerance=0.1)
assert r["rates"] == {"UK": 0.9, "India": 0.7} and r["flag"] and r["underpowered"] == ["Brazil"]
```

A gap usually has a fixable cause (missing local policies in the index, language or terminology differences), so investigate before blaming the model. For any use that affects decisions about people (hiring, performance, credit), fairness assessment is mandatory, involves legal and compliance, and may fall under specific regulation.

## Likely follow-ups

- Why might a quality gap reflect the corpus rather than the model?

---

[← Q0388](../../batch_04_llm_evaluation_observability/0388_reporting_evaluation_results_to_stakeholders/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0390 →](../../batch_04_llm_evaluation_observability/0390_counterfactual_name_swap_test/README.md)

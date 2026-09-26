# Q0350 · Slice evaluation results by segment

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation analysis | Medium |

## Question

Overall accuracy is 91%, but some segments may be failing. Implement slicing by tag (language, business line, query type) with counts, and flag slices below a threshold that have enough support to trust.

## Answer

```python
from collections import defaultdict


def slice_report(results: list[dict], threshold: float, min_support: int = 20) -> dict:
    agg: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for r in results:
        for tag in r["tags"]:
            agg[tag][0] += r["correct"]
            agg[tag][1] += 1
    report = {tag: {"accuracy": c / n, "n": n} for tag, (c, n) in agg.items()}
    flagged = sorted(t for t, v in report.items() if v["n"] >= min_support and v["accuracy"] < threshold)
    return {"slices": report, "flagged": flagged}


results = ([{"tags": ["en", "policy"], "correct": 1}] * 90 + [{"tags": ["fr", "policy"], "correct": 1}] * 14
           + [{"tags": ["fr", "policy"], "correct": 0}] * 11 + [{"tags": ["de"], "correct": 0}] * 3)
r = slice_report(results, threshold=0.8)
assert r["flagged"] == ["fr"] and r["slices"]["fr"]["n"] == 25 and r["slices"]["de"]["n"] == 3
```

French is at 56% while the headline looks healthy. German is also bad but too small to trust, so collect more cases. Slice by the dimensions stakeholders care about and put the slice table in every evaluation report.

## Likely follow-ups

- How do you avoid false alarms when slicing into many small segments?

---

[← Q0349](../../batch_04_llm_evaluation_observability/0349_perturbation_robustness_tests/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0351 →](../../batch_04_llm_evaluation_observability/0351_designing_a_human_evaluation/README.md)

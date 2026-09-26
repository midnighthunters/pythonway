# Q0336 · Report cost and latency percentiles

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation reporting | Easy |

## Question

An evaluation report must include operational metrics. Implement nearest-rank percentiles for latency, total and mean cost, and cost per successful case.

## Answer

```python
import math
from decimal import Decimal


def percentile(values: list[float], p: float) -> float:
    s = sorted(values)
    rank = max(1, math.ceil(p / 100 * len(s)))
    return s[rank - 1]


def ops_report(runs: list[dict]) -> dict:
    lat = [r["latency_ms"] for r in runs]
    cost = sum((r["cost"] for r in runs), Decimal("0"))
    successes = sum(r["success"] for r in runs)
    return {"p50_ms": percentile(lat, 50), "p95_ms": percentile(lat, 95), "p99_ms": percentile(lat, 99),
            "total_cost": cost, "cost_per_success": cost / successes if successes else None}


runs = [{"latency_ms": float(i), "cost": Decimal("0.01"), "success": i % 4 != 0} for i in range(1, 101)]
r = ops_report(runs)
assert (r["p50_ms"], r["p95_ms"], r["p99_ms"]) == (50.0, 95.0, 99.0)
assert r["total_cost"] == Decimal("1.00") and r["cost_per_success"] == Decimal("1.00") / 75
```

Cost per successful task is the fair comparison between a cheap model that fails often (and needs retries or human rework) and an expensive one that succeeds. Report tail latency (p95 and p99), because averages hide the slow cases users actually complain about.

## Likely follow-ups

- Why is the mean latency a misleading headline number?

---

[← Q0335](../../batch_04_llm_evaluation_observability/0335_final_state_evaluation_for_agents/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0337 →](../../batch_04_llm_evaluation_observability/0337_select_a_model_on_the_quality_cost_frontier/README.md)

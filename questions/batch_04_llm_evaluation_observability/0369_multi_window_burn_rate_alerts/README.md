# Q0369 · Multi-window burn-rate alerts

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Reliability engineering | Hard |

## Question

Implement SRE-style multi-window, multi-burn-rate alerting for a 99.9% availability SLO: page when both the 1-hour and 5-minute burn rates exceed 14.4, and raise a ticket when both the 6-hour and 30-minute rates exceed 6.

## Answer

```python
def burn_rate(error_rate: float, slo: float) -> float:
    return error_rate / (1 - slo)


def alert_level(error_rates: dict[str, float], slo: float = 0.999) -> str:
    br = {w: burn_rate(r, slo) for w, r in error_rates.items()}
    if br["1h"] > 14.4 and br["5m"] > 14.4:
        return "page"
    if br["6h"] > 6 and br["30m"] > 6:
        return "ticket"
    return "ok"


assert alert_level({"5m": 0.02, "1h": 0.016, "30m": 0.01, "6h": 0.008}) == "page"
assert alert_level({"5m": 0.001, "1h": 0.016, "30m": 0.008, "6h": 0.007}) == "ticket"
assert alert_level({"5m": 0.0005, "1h": 0.0006, "30m": 0.0005, "6h": 0.0004}) == "ok"
```

A burn rate of 14.4 sustained for an hour consumes 2% of a 30-day budget. The long window proves the problem is significant, and the short window proves it's still happening, which cuts both noisy pages and slow recoveries. In the second case the 1-hour rate is high but the 5-minute rate has recovered, so it becomes a ticket rather than a page. For LLM services, count provider throttling and timeouts as errors, and consider separate SLOs per model route.

## Likely follow-ups

- Why use two windows instead of one?

---

[← Q0368](../../batch_04_llm_evaluation_observability/0368_slo_compliance_and_error_budget_for_ttft/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0370 →](../../batch_04_llm_evaluation_observability/0370_alert_on_an_online_quality_regression/README.md)

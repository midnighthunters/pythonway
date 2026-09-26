# Q0368 · SLO compliance and error budget for TTFT

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Reliability engineering | Medium |

## Question

The SLO is "95% of requests have time to first token under 2,000 ms". Implement the compliance calculation and the share of the error budget consumed.

## Answer

```python
def slo_status(ttft_ms: list[float], threshold_ms: float, objective: float) -> dict:
    good = sum(t <= threshold_ms for t in ttft_ms)
    compliance = good / len(ttft_ms)
    budget = 1 - objective
    bad_fraction = 1 - compliance
    return {"compliance": compliance, "met": compliance >= objective,
            "budget_consumed": bad_fraction / budget if budget else float("inf")}


samples = [800.0] * 970 + [2_500.0] * 30
s = slo_status(samples, 2_000, 0.95)
assert s["compliance"] == 0.97 and s["met"]
assert abs(s["budget_consumed"] - 0.6) < 1e-9
worse = slo_status([800.0] * 930 + [2_500.0] * 70, 2_000, 0.95)
assert not worse["met"] and worse["budget_consumed"] > 1
```

Here 60% of the budget is used, with 97% of requests fast. Error budgets turn reliability into a decision rule: while budget remains, ship changes. When it's exhausted, prioritise reliability work (and, for GenAI, reconsider slower models or larger prompts).

## Likely follow-ups

- Should provider outages count against your SLO?

---

[← Q0367](../../batch_04_llm_evaluation_observability/0367_dashboards_and_slos_for_genai_services/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0369 →](../../batch_04_llm_evaluation_observability/0369_multi_window_burn_rate_alerts/README.md)

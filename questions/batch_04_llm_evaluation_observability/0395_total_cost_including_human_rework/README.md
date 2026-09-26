# Q0395 · Total cost including human rework

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Cost evaluation | Medium |

## Question

Compare two models for a document-extraction workflow where failures need human correction. Compute the all-in cost per document (API cost plus expected rework cost), and show that the cheaper model can be more expensive overall.

## Answer

```python
from decimal import Decimal


def all_in_cost(api_cost: Decimal, success_rate: Decimal, rework_minutes: Decimal, hourly_cost: Decimal) -> Decimal:
    rework = (1 - success_rate) * rework_minutes / 60 * hourly_cost
    return (api_cost + rework).quantize(Decimal("0.0001"))


cheap = all_in_cost(Decimal("0.002"), Decimal("0.85"), Decimal("6"), Decimal("45"))
strong = all_in_cost(Decimal("0.020"), Decimal("0.97"), Decimal("6"), Decimal("45"))
assert cheap == Decimal("0.6770") and strong == Decimal("0.1550")
assert strong < cheap
```

The prices and rates are illustrative. The API cost is a rounding error next to people's time: 15% failures × 6 minutes × £45 per hour dominates. That's why "cost per successful task" and "cost including rework" are the right lenses, not cost per token. A cascade (cheap model first, strong model on low confidence) might beat both, so evaluate it too.

## Likely follow-ups

- How would a confidence-based cascade change these numbers?

---

[← Q0394](../../batch_04_llm_evaluation_observability/0394_ongoing_monitoring_for_model_risk_management/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0396 →](../../batch_04_llm_evaluation_observability/0396_evaluating_code_fix_agents/README.md)

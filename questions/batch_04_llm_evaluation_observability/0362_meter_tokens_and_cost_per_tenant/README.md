# Q0362 · Meter tokens and cost per tenant

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Cost observability | Medium |

## Question

Implement usage metering for a shared LLM gateway: record tokens per tenant and model, price them with a rate table, and raise budget alerts at 80% and 100% of each tenant's monthly budget (only once per threshold).

## Answer

```python
from collections import defaultdict
from decimal import Decimal

RATES = {"small": (Decimal("0.15"), Decimal("0.60")), "large": (Decimal("2.50"), Decimal("10.00"))}


class Meter:
    def __init__(self, budgets: dict[str, Decimal]) -> None:
        self.budgets = budgets
        self.spend: dict[str, Decimal] = defaultdict(Decimal)
        self.tokens: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])
        self.alerts: list[tuple[str, int]] = []
        self._fired: set[tuple[str, int]] = set()

    def record(self, tenant: str, model: str, input_tokens: int, output_tokens: int) -> Decimal:
        rin, rout = RATES[model]
        cost = (input_tokens * rin + output_tokens * rout) / 1_000_000
        self.spend[tenant] += cost
        t = self.tokens[(tenant, model)]
        t[0] += input_tokens
        t[1] += output_tokens
        used = self.spend[tenant] / self.budgets[tenant] * 100
        for pct in (80, 100):
            if used >= pct and (tenant, pct) not in self._fired:
                self._fired.add((tenant, pct))
                self.alerts.append((tenant, pct))
        return cost


m = Meter({"treasury": Decimal("10.00")})
m.record("treasury", "large", 2_000_000, 200_000)
assert m.spend["treasury"] == Decimal("7.00") and m.alerts == []
m.record("treasury", "large", 400_000, 0)
m.record("treasury", "small", 1_000_000, 0)
assert m.alerts == [("treasury", 80)]
m.record("treasury", "large", 1_000_000, 0)
assert m.alerts == [("treasury", 80), ("treasury", 100)] and m.tokens[("treasury", "large")] == [3_400_000, 200_000]
```

Prefer the provider's reported usage over your own estimates for billing. Decide the policy at 100% (block, degrade to a cheaper model, or alert only) with each tenant. Emit this as metrics (not just logs), so dashboards and chargeback reports use the same numbers.

## Likely follow-ups

- How would you attribute the cost of a shared system prompt across tenants?

---

[← Q0361](../../batch_04_llm_evaluation_observability/0361_tracing_decorator_with_nested_spans/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0363 →](../../batch_04_llm_evaluation_observability/0363_structured_json_logs_for_llm_calls/README.md)

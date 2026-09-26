# Q0440 · Token and cost budget manager

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Cost control | Medium |

## Question

Implement a per-run budget manager: reserve an estimated cost before each LLM or tool call, commit the actual cost afterwards (releasing the unused reservation), and refuse calls that would exceed the budget.

## Answer

```python
from decimal import Decimal


class BudgetExceeded(Exception):
    pass


class Budget:
    def __init__(self, limit: Decimal) -> None:
        self.limit, self.spent, self.reserved = limit, Decimal("0"), Decimal("0")

    def reserve(self, estimate: Decimal) -> Decimal:
        if self.spent + self.reserved + estimate > self.limit:
            raise BudgetExceeded(f"need {estimate}, remaining {self.limit - self.spent - self.reserved}")
        self.reserved += estimate
        return estimate

    def commit(self, reservation: Decimal, actual: Decimal) -> None:
        self.reserved -= reservation
        self.spent += actual

    @property
    def remaining(self) -> Decimal:
        return self.limit - self.spent - self.reserved


b = Budget(Decimal("0.10"))
r1 = b.reserve(Decimal("0.04"))
b.commit(r1, Decimal("0.03"))
r2 = b.reserve(Decimal("0.05"))
assert b.remaining == Decimal("0.02")
try:
    b.reserve(Decimal("0.03"))
    raise AssertionError
except BudgetExceeded:
    pass
b.commit(r2, Decimal("0.05"))
assert b.spent == Decimal("0.08") and b.remaining == Decimal("0.02")
```

Reserving before the call (prompt tokens plus `max_tokens` at list price) stops parallel calls from overshooting together. When the budget runs low, degrade gracefully: switch to a cheaper model, skip optional steps, or wrap up with the best answer so far. Record the per-run cost in traces.

## Likely follow-ups

- What should the agent do when it has 10% of its budget left and isn't finished?

---

[← Q0439](../../batch_05_agentic_patterns_orchestration/0439_sub_agents_to_isolate_context/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0441 →](../../batch_05_agentic_patterns_orchestration/0441_choose_a_model_per_step/README.md)

# Q0441 · Choose a model per step

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Cost control | Medium |

## Question

Implement step-level model routing: cheap models for routing and extraction, strong models for planning and synthesis, with escalation to the next tier when a step's output fails validation.

## Answer

```python
from typing import Callable

TIERS = ["small", "medium", "large"]
DEFAULT_TIER = {"route": "small", "extract": "small", "plan": "large", "synthesize": "medium"}


def run_step(step: str, payload: str, models: dict[str, Callable[[str], str]],
             valid: Callable[[str], bool]) -> tuple[str, str]:
    start = TIERS.index(DEFAULT_TIER.get(step, "medium"))
    for tier in TIERS[start:]:
        out = models[tier](payload)
        if valid(out):
            return tier, out
    raise RuntimeError(f"step {step} failed validation at every tier")


models = {"small": lambda p: "garbage" if "tricky" in p else '{"amount": "10.00"}',
          "medium": lambda p: '{"amount": "10.00"}', "large": lambda p: '{"amount": "10.00"}'}
is_json = lambda s: s.startswith("{")
assert run_step("extract", "simple receipt", models, is_json) == ("small", '{"amount": "10.00"}')
assert run_step("extract", "tricky receipt", models, is_json)[0] == "medium"
assert run_step("plan", "anything", models, is_json)[0] == "large"
```

Validation-driven escalation only pays when there is a reliable validator (a schema, business rules or tests). Log the escalation rate per step: a high rate means the default tier is wrong for that step, and you're paying for two calls.

## Likely follow-ups

- When is it cheaper to always use the larger model for a step?

---

[← Q0440](../../batch_05_agentic_patterns_orchestration/0440_token_and_cost_budget_manager/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0442 →](../../batch_05_agentic_patterns_orchestration/0442_final_answer_schema_for_agents/README.md)

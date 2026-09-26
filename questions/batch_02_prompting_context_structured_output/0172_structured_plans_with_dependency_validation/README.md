# Q0172 · Structured plans with dependency validation

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Planning | Medium |

## Question

An agent's planner returns a JSON plan of steps with ids, a tool and `depends_on`. Validate it with Pydantic: unique ids, known tools, a bounded number of steps, and dependencies only on earlier steps (which guarantees a DAG).

## Answer

```python
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, model_validator


class Step(BaseModel):
    id: int = Field(ge=1)
    tool: Literal["search_policies", "get_balance", "draft_email", "ask_user"]
    input: str
    depends_on: list[int] = []


class Plan(BaseModel):
    goal: str
    steps: list[Step] = Field(min_length=1, max_length=8)

    @model_validator(mode="after")
    def check_graph(self) -> "Plan":
        seen: set[int] = set()
        for s in self.steps:
            if s.id in seen:
                raise ValueError(f"duplicate step id {s.id}")
            bad = [d for d in s.depends_on if d not in seen]
            if bad:
                raise ValueError(f"step {s.id} depends on unknown or later steps {bad}")
            seen.add(s.id)
        return self


plan = Plan.model_validate({"goal": "Email manager about travel limit", "steps": [
    {"id": 1, "tool": "search_policies", "input": "travel limit"},
    {"id": 2, "tool": "draft_email", "input": "summary for manager", "depends_on": [1]}]})
assert [s.id for s in plan.steps] == [1, 2]
for steps in ([{"id": 1, "tool": "search_policies", "input": "x", "depends_on": [2]},
               {"id": 2, "tool": "draft_email", "input": "y"}],
              [{"id": 1, "tool": "wire_money", "input": "x"}]):
    try:
        Plan.model_validate({"goal": "g", "steps": steps})
        raise AssertionError
    except ValidationError:
        pass
```

Requiring dependencies to point backwards rules out cycles without a graph algorithm. Once validated, independent steps (no mutual dependencies) can run in parallel. Keep the ability to re-plan when a step fails.

## Likely follow-ups

- How would you execute this plan with maximum parallelism?

---

[← Q0171](../../batch_02_prompting_context_structured_output/0171_strip_scratchpad_content_before_display/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0173 →](../../batch_02_prompting_context_structured_output/0173_handle_refusals_in_structured_output/README.md)

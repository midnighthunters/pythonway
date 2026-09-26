# Q0334 · Agent trajectory evaluation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Agent evaluation | Medium |

## Question

Evaluate agent trajectories against a specification: required milestone tools must appear in order (as a subsequence), forbidden tools must never be called, and the step count must stay within a budget.

## Answer

```python
def evaluate_trajectory(calls: list[str], milestones: list[str], forbidden: set[str], max_steps: int) -> dict:
    it = iter(calls)
    in_order = all(m in it for m in milestones)
    violations = sorted(set(calls) & forbidden)
    return {"milestones_in_order": in_order, "forbidden_calls": violations,
            "within_budget": len(calls) <= max_steps,
            "pass": in_order and not violations and len(calls) <= max_steps}


spec = {"milestones": ["lookup_booking", "search_flights", "confirm_with_user", "rebook"],
        "forbidden": {"issue_refund"}, "max_steps": 8}
good = ["lookup_booking", "search_flights", "search_flights", "confirm_with_user", "rebook"]
bad_order = ["lookup_booking", "rebook", "confirm_with_user"]
risky = ["lookup_booking", "search_flights", "issue_refund", "confirm_with_user", "rebook"]
assert evaluate_trajectory(good, **spec)["pass"]
assert not evaluate_trajectory(bad_order, **spec)["milestones_in_order"]
assert evaluate_trajectory(risky, **spec)["forbidden_calls"] == ["issue_refund"]
```

The `m in it` trick consumes the iterator, so it checks that the milestones appear in order with anything allowed in between. Trajectory checks catch unsafe paths (rebooking before the user confirmed) even when the final answer looks fine. Combine them with final-state checks and task-success judges.

## Likely follow-ups

- When should trajectory evaluation be strict, and when should it be flexible?

---

[← Q0333](../../batch_04_llm_evaluation_observability/0333_evaluating_tool_calling_accuracy/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0335 →](../../batch_04_llm_evaluation_observability/0335_final_state_evaluation_for_agents/README.md)

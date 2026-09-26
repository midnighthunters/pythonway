# Q0117 · Allocate a token budget across context sections

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

Implement a token budget allocator: each context section has a minimum, a desired amount and a priority. Give every section its minimum, then hand out the remaining budget in priority order up to each section's desired size. Fail if the minimums don't fit.

## Answer

```python
def allocate_budget(sections: list[dict], budget: int) -> dict[str, int]:
    """sections: {name, min, want, priority} where a lower priority number is more important."""
    total_min = sum(s["min"] for s in sections)
    if total_min > budget:
        raise ValueError(f"minimums need {total_min} tokens, budget is {budget}")
    alloc = {s["name"]: s["min"] for s in sections}
    remaining = budget - total_min
    for s in sorted(sections, key=lambda s: s["priority"]):
        extra = min(remaining, max(0, s["want"] - s["min"]))
        alloc[s["name"]] += extra
        remaining -= extra
    return alloc


sections = [
    {"name": "system", "min": 800, "want": 800, "priority": 0},
    {"name": "question", "min": 200, "want": 200, "priority": 0},
    {"name": "retrieved", "min": 1_000, "want": 6_000, "priority": 1},
    {"name": "history", "min": 0, "want": 4_000, "priority": 2},
]
assert allocate_budget(sections, 8_000) == {"system": 800, "question": 200, "retrieved": 6_000, "history": 1_000}
assert allocate_budget(sections, 3_000) == {"system": 800, "question": 200, "retrieved": 2_000, "history": 0}
try:
    allocate_budget(sections, 1_500)
    raise AssertionError
except ValueError:
    pass
```

Each section then trims or summarises itself to its allocation. Reserve output tokens separately, before allocating the input budget.

## Likely follow-ups

- Should retrieved context or conversation history get priority, and does it depend on the turn?

---

[← Q0116](../../batch_02_prompting_context_structured_output/0116_what_context_engineering_means/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0118 →](../../batch_02_prompting_context_structured_output/0118_trim_conversation_history_without_breaking_tool_pairs/README.md)

# Q0408 · Detect cyclic tool-call patterns

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent safety | Medium |

## Question

Agents sometimes oscillate between two or three actions (A, B, A, B…). Implement cycle detection on the recent call sequence for any period up to half the history.

## Answer

```python
def detect_cycle(calls: list[str], min_repeats: int = 3, max_period: int = 4) -> int | None:
    """Return the period p if the tail of `calls` is the same p-length block repeated min_repeats times."""
    for p in range(1, max_period + 1):
        needed = p * min_repeats
        if len(calls) < needed:
            break
        tail = calls[-needed:]
        block = tail[:p]
        if all(tail[i] == block[i % p] for i in range(needed)):
            return p
    return None


assert detect_cycle(["search", "read", "search", "read", "search", "read"]) == 2
assert detect_cycle(["a", "a", "a"]) == 1
assert detect_cycle(["plan", "search", "read", "answer"]) is None
assert detect_cycle(["x", "a", "b", "c", "a", "b", "c", "a", "b", "c"]) == 3
```

Include the arguments in each call signature when they matter (alternating searches with different queries may be legitimate progress). On detection, inject a reflection prompt ("You seem to be repeating X and Y. Summarise what you know and choose a different approach or finish"), or stop and escalate.

## Likely follow-ups

- How would you distinguish a legitimate polling loop from an unproductive cycle?

---

[← Q0407](../../batch_05_agentic_patterns_orchestration/0407_loop_guards_steps_tokens_and_repetition/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0409 →](../../batch_05_agentic_patterns_orchestration/0409_plan_and_execute_agent/README.md)

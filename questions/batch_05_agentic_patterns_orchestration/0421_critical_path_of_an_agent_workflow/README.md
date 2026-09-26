# Q0421 · Critical path of an agent workflow

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Orchestration | Medium |

## Question

Given task durations and dependencies, compute the critical path (the longest chain that determines total latency), to know which step to optimise.

## Answer

```python
from functools import lru_cache


def critical_path(durations: dict[str, float], deps: dict[str, set[str]]) -> tuple[float, list[str]]:
    @lru_cache(maxsize=None)
    def finish(node: str) -> tuple[float, tuple[str, ...]]:
        best = (0.0, ())
        for d in deps.get(node, set()):
            best = max(best, finish(d))
        return best[0] + durations[node], best[1] + (node,)

    total, path = max(finish(n) for n in durations)
    return total, list(path)


durations = {"plan": 1.2, "search_flights": 2.5, "search_hotels": 1.0, "check_policy": 0.4, "compose": 1.5}
deps = {"search_flights": {"plan"}, "search_hotels": {"plan"}, "check_policy": {"search_flights", "search_hotels"},
        "compose": {"check_policy"}}
total, path = critical_path(durations, deps)
assert abs(total - 5.6) < 1e-9 and path == ["plan", "search_flights", "check_policy", "compose"]
```

Speeding up `search_hotels` does nothing, because it isn't on the critical path. Optimise `search_flights` (cache it, use a faster API, return early with partial results) or the LLM steps (a smaller planner model, streaming the compose step). Use p95 durations from traces, not averages.

## Likely follow-ups

- How does the critical path change when a step has retries?

---

[← Q0420](../../batch_05_agentic_patterns_orchestration/0420_execute_a_task_graph_with_maximum_parallelism/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0422 →](../../batch_05_agentic_patterns_orchestration/0422_saga_pattern_for_multi_step_bookings/README.md)

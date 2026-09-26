# Q0419 · Topological sort of a task graph

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Orchestration | Medium |

## Question

An orchestrator receives tasks with dependencies. Implement Kahn's algorithm to produce an execution order, grouped into parallel "waves", and detect cycles with a helpful error.

## Answer

```python
from collections import deque


def execution_waves(deps: dict[str, set[str]]) -> list[list[str]]:
    nodes = set(deps) | {d for ds in deps.values() for d in ds}
    indeg = {n: 0 for n in nodes}
    children: dict[str, list[str]] = {n: [] for n in nodes}
    for n, ds in deps.items():
        for d in ds:
            indeg[n] += 1
            children[d].append(n)
    ready = deque(sorted(n for n in nodes if indeg[n] == 0))
    waves, seen = [], 0
    while ready:
        wave = sorted(ready)
        ready.clear()
        waves.append(wave)
        seen += len(wave)
        for n in wave:
            for c in children[n]:
                indeg[c] -= 1
                if indeg[c] == 0:
                    ready.append(c)
    if seen != len(nodes):
        stuck = sorted(n for n, d in indeg.items() if d > 0)
        raise ValueError(f"cycle detected among: {stuck}")
    return waves


deps = {"fetch_trades": set(), "fetch_positions": set(), "reconcile": {"fetch_trades", "fetch_positions"},
        "report": {"reconcile"}, "notify": {"report"}}
assert execution_waves(deps) == [["fetch_positions", "fetch_trades"], ["reconcile"], ["report"], ["notify"]]
try:
    execution_waves({"a": {"b"}, "b": {"a"}})
    raise AssertionError
except ValueError as e:
    assert "cycle" in str(e)
```

Waves show the parallelism: everything in a wave can run concurrently. Validate LLM-generated plans this way before executing them, since models can produce cyclic or dangling dependencies.

## Likely follow-ups

- How would you add a dependency on a task that doesn't exist to the error message?

---

[← Q0418](../../batch_05_agentic_patterns_orchestration/0418_fan_out_and_fan_in_with_bounded_concurrency/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0420 →](../../batch_05_agentic_patterns_orchestration/0420_execute_a_task_graph_with_maximum_parallelism/README.md)

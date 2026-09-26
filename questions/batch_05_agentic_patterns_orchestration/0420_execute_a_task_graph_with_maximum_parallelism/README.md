# Q0420 · Execute a task graph with maximum parallelism

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Orchestration | Hard |

## Question

Implement an async DAG executor: start each task as soon as its dependencies succeed, run independent tasks concurrently, and mark dependents of a failed task as skipped.

## Answer

```python
import asyncio
from typing import Awaitable, Callable


async def run_dag(tasks: dict[str, tuple[set[str], Callable[[dict], Awaitable]]]) -> dict[str, dict]:
    results: dict[str, dict] = {}
    done_events = {name: asyncio.Event() for name in tasks}

    async def run(name: str) -> None:
        deps, fn = tasks[name]
        for d in deps:
            await done_events[d].wait()
        if any(results[d]["status"] != "ok" for d in deps):
            results[name] = {"status": "skipped"}
        else:
            try:
                value = await fn({d: results[d]["value"] for d in deps})
                results[name] = {"status": "ok", "value": value}
            except Exception as e:
                results[name] = {"status": "failed", "error": str(e)}
        done_events[name].set()

    await asyncio.gather(*(run(n) for n in tasks))
    return results


order: list[str] = []


def step(name: str, value=None, fail: bool = False, delay: float = 0.01):
    async def fn(inputs: dict):
        order.append(f"start:{name}")
        await asyncio.sleep(delay)
        if fail:
            raise RuntimeError(f"{name} failed")
        return value if value is not None else sum(inputs.values())
    return fn


tasks = {
    "a": (set(), step("a", 1)), "b": (set(), step("b", 2)),
    "c": ({"a", "b"}, step("c")), "d": ({"a"}, step("d", fail=True)), "e": ({"d"}, step("e")),
}
res = asyncio.run(run_dag(tasks))
assert res["c"] == {"status": "ok", "value": 3}
assert res["d"]["status"] == "failed" and res["e"] == {"status": "skipped"}
assert set(order[:2]) == {"start:a", "start:b"}
```

Validate the graph first (topological sort, no missing dependencies), because a missing dependency would wait forever here. Add per-task timeouts, retries for idempotent tasks, and checkpointing of results, so a crash doesn't redo finished work.

## Likely follow-ups

- How would you add a global concurrency limit?

---

[← Q0419](../../batch_05_agentic_patterns_orchestration/0419_topological_sort_of_a_task_graph/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0421 →](../../batch_05_agentic_patterns_orchestration/0421_critical_path_of_an_agent_workflow/README.md)

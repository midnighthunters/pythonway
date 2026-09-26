# Q0494 · Fair scheduling of agent jobs across tenants

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Platform architecture | Hard |

## Question

Background agent jobs from many tenants share a worker pool. Implement weighted deficit round robin, so each tenant gets throughput proportional to its weight, and a flood from one tenant can't starve the others.

## Answer

```python
from collections import deque


def deficit_round_robin(queues: dict[str, deque], weights: dict[str, int], quantum: int = 10,
                        max_jobs: int = 100) -> list[tuple[str, str]]:
    deficit = {t: 0 for t in queues}
    order: list[tuple[str, str]] = []
    while any(queues.values()) and len(order) < max_jobs:
        for tenant, q in queues.items():
            if not q:
                deficit[tenant] = 0
                continue
            deficit[tenant] += quantum * weights[tenant]
            while q and q[0]["cost"] <= deficit[tenant] and len(order) < max_jobs:
                job = q.popleft()
                deficit[tenant] -= job["cost"]
                order.append((tenant, job["id"]))
    return order


queues = {
    "treasury": deque({"id": f"t{i}", "cost": 10} for i in range(50)),
    "hr": deque({"id": f"h{i}", "cost": 10} for i in range(3)),
    "risk": deque({"id": f"r{i}", "cost": 20} for i in range(10)),
}
order = deficit_round_robin(queues, {"treasury": 1, "hr": 1, "risk": 2}, max_jobs=12)
first12 = [t for t, _ in order]
assert first12.count("hr") == 3 and first12.count("risk") >= 3 and first12.count("treasury") <= 6
```

Costs can be estimated tokens or run time, so heavy jobs count more than light ones. HR's three jobs all run within the first rounds despite Treasury's 50-job flood. Combine this with per-tenant concurrency caps and priority classes (interactive over background).

## Likely follow-ups

- How would you add a priority lane for interactive requests without starving batch jobs?

---

[← Q0493](../../batch_05_agentic_patterns_orchestration/0493_slos_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0495 →](../../batch_05_agentic_patterns_orchestration/0495_backpressure_in_agent_pipelines/README.md)

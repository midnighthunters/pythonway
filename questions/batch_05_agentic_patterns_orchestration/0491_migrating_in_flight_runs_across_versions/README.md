# Q0491 · Migrating in-flight runs across versions

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Operations | Medium |

## Question

Some agent runs wait days for approvals. When you deploy a new version with a changed state schema, how do you handle in-flight runs? Implement a chained state upgrader.

## Answer

```python
def v1_to_v2(s: dict) -> dict:
    s = dict(s)
    s["approvals"] = [s.pop("approval")] if s.get("approval") else []
    return {**s, "schema": 2}


def v2_to_v3(s: dict) -> dict:
    return {**s, "budget": s.get("budget", {"limit": "1.00", "spent": "0.00"}), "schema": 3}


MIGRATIONS = {1: v1_to_v2, 2: v2_to_v3}
CURRENT = 3


def upgrade(state: dict) -> dict:
    s = dict(state)
    while s.get("schema", 1) < CURRENT:
        s = MIGRATIONS[s.get("schema", 1)](s)
    return s


old = {"schema": 1, "task": "refund INV-7", "approval": {"ticket": 12, "status": "pending"}}
new = upgrade(old)
assert new == {"schema": 3, "task": "refund INV-7", "approvals": [{"ticket": 12, "status": "pending"}],
               "budget": {"limit": "1.00", "spent": "0.00"}}
assert upgrade(new) == new
```

Strategies:
- Pinning: in-flight runs continue on the old version's code, and new runs start on the new version. This is safest, but you must keep old workers running until drained (workflow engines support this).
- Migrating: upgrade the state on load with chained, tested migrations (as above), so every version can read old checkpoints.
- For behavioural changes mid-run (a new approval step), decide explicitly: either apply it from the next step, or only to new runs.

Test migrations against real checkpoint samples, and never delete old code paths while runs still depend on them.

## Likely follow-ups

- When would you pin rather than migrate?

---

[← Q0490](../../batch_05_agentic_patterns_orchestration/0490_versioning_agents_and_workflows/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0492 →](../../batch_05_agentic_patterns_orchestration/0492_multi_tenant_agent_platform_concerns/README.md)

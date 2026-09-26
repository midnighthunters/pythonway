# Q0454 · Locks when agents share resources

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Concurrency | Medium |

## Question

Two agent runs may update the same account concurrently. Implement per-key async locks so updates to the same key are serialised, while different keys proceed in parallel.

## Answer

```python
import asyncio
from collections import defaultdict


class KeyedLocks:
    def __init__(self) -> None:
        self._locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    def __call__(self, key: str) -> asyncio.Lock:
        return self._locks[key]


balances = {"ACC-1": 100, "ACC-2": 100}
locks = KeyedLocks()
concurrent_keys: list[set[str]] = []
active: set[str] = set()


async def debit(account: str, amount: int) -> None:
    async with locks(account):
        active.add(account)
        concurrent_keys.append(set(active))
        current = balances[account]
        await asyncio.sleep(0.01)
        balances[account] = current - amount
        active.discard(account)


async def main() -> None:
    await asyncio.gather(*(debit("ACC-1", 10) for _ in range(5)), *(debit("ACC-2", 5) for _ in range(5)))


asyncio.run(main())
assert balances == {"ACC-1": 50, "ACC-2": 75}
assert any(s == {"ACC-1", "ACC-2"} for s in concurrent_keys)
```

Without the lock, the read-sleep-write sequence would lose updates. In-process locks only protect one process. Across replicas, use database transactions (`SELECT … FOR UPDATE`), optimistic concurrency (next question) or a distributed lock with leases (and fencing tokens, because leases can expire mid-operation).

## Likely follow-ups

- Why do distributed locks need fencing tokens?

---

[← Q0453](../../batch_05_agentic_patterns_orchestration/0453_scheduled_and_background_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0455 →](../../batch_05_agentic_patterns_orchestration/0455_optimistic_concurrency_for_agent_writes/README.md)

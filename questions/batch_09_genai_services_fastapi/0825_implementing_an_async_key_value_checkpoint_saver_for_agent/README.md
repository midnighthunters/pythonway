# Q0825 · Implementing an async key-value checkpoint saver for agent graphs

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Hard |

## Question

Write Python code implementing an asynchronous checkpoint saver for agent state graphs, supporting saving versioned state snapshots and restoring the latest checkpoint by thread ID.

## Answer

In distributed multi-agent systems, saving execution checkpoints after each node execution allows the system to resume interrupted runs, support human-in-the-loop approvals, and inspect past agent states.

```python
import asyncio
from typing import Any, Dict, List, Optional


class AsyncKeyValueCheckpointSaver:
    def __init__(self):
        # Structure: thread_id -> list of checkpoints sorted by version
        self._storage: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = asyncio.Lock()

    async def aput(self, thread_id: str, state: Dict[str, Any], metadata: Optional[Dict] = None) -> int:
        async with self._lock:
            if thread_id not in self._storage:
                self._storage[thread_id] = []
            version = len(self._storage[thread_id]) + 1
            checkpoint = {
                "version": version,
                "state": state.copy(),
                "metadata": metadata or {},
            }
            self._storage[thread_id].append(checkpoint)
            return version

    async def aget_latest(self, thread_id: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            history = self._storage.get(thread_id)
            if not history:
                return None
            return history[-1]

    async def aget_version(self, thread_id: str, version: int) -> Optional[Dict[str, Any]]:
        async with self._lock:
            history = self._storage.get(thread_id, [])
            for cp in history:
                if cp["version"] == version:
                    return cp
            return None


async def main():
    saver = AsyncKeyValueCheckpointSaver()
    v1 = await saver.aput("th_001", {"messages": ["What is Basel III?"], "step": 1})
    v2 = await saver.aput("th_001", {"messages": ["What is Basel III?", "Basel III is..."], "step": 2})
    assert v1 == 1 and v2 == 2

    latest = await saver.aget_latest("th_001")
    assert latest["version"] == 2
    assert latest["state"]["step"] == 2

    old = await saver.aget_version("th_001", 1)
    assert old["version"] == 1
    assert len(old["state"]["messages"]) == 1


asyncio.run(main())
```

## Likely follow-ups

- How does LangGraph's `MemorySaver` vs `AsyncSqliteSaver` vs `AsyncPostgresSaver` implement this abstraction?
- What strategy prevents unbounded checkpoint storage growth in long-running threads?

---

[← Q0824](../../batch_09_genai_services_fastapi/0824_redis_vs_dynamodb_vs_postgresql_for_conversation_state/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0826 →](../../batch_09_genai_services_fastapi/0826_conversation_history_pruning_and_summarization_triggers/README.md)

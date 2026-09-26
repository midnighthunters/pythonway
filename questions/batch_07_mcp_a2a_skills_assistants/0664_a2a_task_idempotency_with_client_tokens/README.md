# Q0664 · A2A task idempotency with client tokens

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Write Python code implementing an idempotency store for A2A task submissions, ensuring network retries with the same `Idempotency-Key` do not create duplicate tasks.

## Answer

Due to network timeouts, clients frequently retry `POST /tasks`. The server must use the `Idempotency-Key` header to return the existing task rather than spawning duplicate expensive workflows.

```python
from typing import Any, Dict, Optional, Tuple


class IdempotentTaskStore:
    def __init__(self):
        self._keys: Dict[str, str] = {}
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def submit_task(self, idempotency_key: str, payload: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        if idempotency_key in self._keys:
            existing_task_id = self._keys[idempotency_key]
            return self._tasks[existing_task_id], False

        new_task_id = f"task-{len(self._tasks) + 1}"
        record = {"task_id": new_task_id, "status": "submitted", "payload": payload}
        self._keys[idempotency_key] = new_task_id
        self._tasks[new_task_id] = record
        return record, True


store = IdempotentTaskStore()
task1, created1 = store.submit_task("req-key-001", {"query": "Check limits"})
assert created1 is True
assert task1["task_id"] == "task-1"

# Duplicate retry
task2, created2 = store.submit_task("req-key-001", {"query": "Check limits"})
assert created2 is False
assert task2["task_id"] == "task-1"
```

## Likely follow-ups

- How long should an idempotency key be cached in an enterprise Redis store?
- What should happen if a retry arrives with the same key but a different payload?

---

[← Q0663](../../batch_07_mcp_a2a_skills_assistants/0663_a2a_thread_and_context_propagation/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0665 →](../../batch_07_mcp_a2a_skills_assistants/0665_building_an_in_memory_a2a_task_engine/README.md)

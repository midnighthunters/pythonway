# Q0820 · Optimistic concurrency control for parallel agent state updates

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Hard |

## Question

What is Optimistic Concurrency Control (OCC), and write Python code implementing OCC with version numbers to prevent race conditions during concurrent agent state writes.

## Answer

When two parallel agent branches (e.g. Risk Evaluator and Compliance Checker) update a shared thread state simultaneously, standard writes cause the "last-write-wins" problem, silently overwriting earlier findings.

OCC Mechanism:
- Every state record includes a `version` integer.
- Updates require a conditional check: `UPDATE table SET data = new_data, version = version + 1 WHERE id = thread_id AND version = current_version`.
- If another worker incremented the version first, the write is rejected with a concurrency conflict. The rejected worker rereads the latest state and retries.

```python
from typing import Any, Dict


class OCCStateStore:
    def __init__(self):
        self._records: Dict[str, Dict[str, Any]] = {}

    def init_record(self, key: str, data: Any) -> None:
        self._records[key] = {"data": data, "version": 1}

    def update_record(self, key: str, expected_version: int, new_data: Any) -> bool:
        rec = self._records.get(key)
        if not rec:
            return False

        if rec["version"] != expected_version:
            # Concurrency conflict: record was modified by another branch
            return False

        rec["data"] = new_data
        rec["version"] += 1
        return True

    def get_record(self, key: str) -> Dict[str, Any]:
        return self._records.get(key, {})


store = OCCStateStore()
store.init_record("thread_1", {"findings": []})

# Branch A reads version 1
branch_a = store.get_record("thread_1")
assert branch_a["version"] == 1

# Branch B reads version 1
branch_b = store.get_record("thread_1")
assert branch_b["version"] == 1

# Branch A writes successfully -> version becomes 2
ok_a = store.update_record("thread_1", expected_version=1, new_data={"findings": ["Risk: OK"]})
assert ok_a is True

# Branch B attempts to write with stale version 1 -> rejected!
ok_b = store.update_record("thread_1", expected_version=1, new_data={"findings": ["Compliance: Flagged"]})
assert ok_b is False  # Race condition prevented!
```

## Likely follow-ups

- How does DynamoDB `attribute_exists` and `ConditionExpression` implement OCC natively?
- How should the rejected agent branch merge its updates with the newly committed state?

---

[← Q0819](../../batch_09_genai_services_fastapi/0819_dynamodb_thread_history_repository_implementation_in_python/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0821 →](../../batch_09_genai_services_fastapi/0821_redis_ttl_session_store_with_sliding_window_expiration/README.md)

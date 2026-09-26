# Q0819 · DynamoDB thread history repository implementation in Python

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Write Python code implementing an in-memory dictionary-backed repository simulating DynamoDB message retrieval with timestamp range filtering and limit pagination.

## Answer

```python
from typing import Any, Dict, List, Optional


class SimulatedNoSQLConversationStore:
    def __init__(self):
        # Maps PK -> list of message items sorted by SK
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def append_message(self, tenant_id: str, thread_id: str, message_id: str, timestamp: str, role: str, content: str) -> None:
        pk = f"TENANT#{tenant_id}#THREAD#{thread_id}"
        sk = f"MSG#{timestamp}#{message_id}"
        if pk not in self._store:
            self._store[pk] = []
        self._store[pk].append({"PK": pk, "SK": sk, "role": role, "content": content})
        self._store[pk].sort(key=lambda x: x["SK"])

    def get_messages(self, tenant_id: str, thread_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        pk = f"TENANT#{tenant_id}#THREAD#{thread_id}"
        return self._store.get(pk, [])[:limit]


store = SimulatedNoSQLConversationStore()
store.append_message("t1", "th-100", "m1", "2026-09-26T10:00:00Z", "user", "What is EURUSD spot?")
store.append_message("t1", "th-100", "m2", "2026-09-26T10:00:02Z", "assistant", "EURUSD is 1.0850.")

history = store.get_messages("t1", "th-100", limit=5)
assert len(history) == 2
assert history[0]["role"] == "user"
assert history[1]["content"] == "EURUSD is 1.0850."
```

## Likely follow-ups

- How does point-in-time recovery (PITR) in DynamoDB satisfy regulatory data protection standards?
- How do you implement message deletion under GDPR Article 17 ("Right to Erasure") in NoSQL?

---

[← Q0818](../../batch_09_genai_services_fastapi/0818_storing_conversation_history_in_nosql_dynamodb_and_cosmos_db/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0820 →](../../batch_09_genai_services_fastapi/0820_optimistic_concurrency_control_for_parallel_agent_state/README.md)

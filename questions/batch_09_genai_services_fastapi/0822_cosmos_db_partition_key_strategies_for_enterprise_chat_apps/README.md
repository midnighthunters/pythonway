# Q0822 · Cosmos DB partition key strategies for enterprise chat apps

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Explain how to choose an optimal partition key in Azure Cosmos DB for a multi-tenant corporate chat application, and write Python code simulating partition-based query filtering.

## Answer

In Azure Cosmos DB, choosing an improper partition key leads to "hot partitions" where one physical partition exceeds the 20 GB storage limit or 10,000 RU/s throughput ceiling.

In enterprise multi-tenant GenAI services:
1. `tenant_id` alone creates a hot partition if one large organization generates millions of messages.
2. `session_id` (or `thread_id`) spreads data evenly across partitions, ensuring single-turn history queries target exactly one partition key without expensive cross-partition fan-out queries.
3. A composite synthetic key such as `tenant_id#user_id` or `tenant_id#thread_id` provides tenant isolation while avoiding single-tenant throttling.

```python
from typing import Dict, List, Optional


class CosmosDBChatContainer:
    def __init__(self):
        # Simulated Cosmos DB container partitioned by thread_id
        self.items: Dict[str, List[Dict]] = {}

    def insert_item(self, doc: dict) -> None:
        partition_key = doc["thread_id"]
        if partition_key not in self.items:
            self.items[partition_key] = []
        self.items[partition_key].append(doc)

    def query_by_thread(self, thread_id: str) -> List[Dict]:
        # Single-partition query: highly efficient (1-2 RUs)
        return self.items.get(thread_id, [])


db = CosmosDBChatContainer()
db.insert_item({"id": "m1", "thread_id": "th_abc", "role": "user", "text": "Hi"})
db.insert_item({"id": "m2", "thread_id": "th_abc", "role": "assistant", "text": "Welcome"})
db.insert_item({"id": "m3", "thread_id": "th_xyz", "role": "user", "text": "Trade status"})

results = db.query_by_thread("th_abc")
assert len(results) == 2
assert all(r["thread_id"] == "th_abc" for r in results)
```

## Likely follow-ups

- What are the operational costs of cross-partition queries in Cosmos DB?
- How does Cosmos DB Request Unit (RU) consumption scale with document size?

---

[← Q0821](../../batch_09_genai_services_fastapi/0821_redis_ttl_session_store_with_sliding_window_expiration/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0823 →](../../batch_09_genai_services_fastapi/0823_mongodb_document_schema_design_for_hierarchical_agent_traces/README.md)

# Q0830 · Read consistency models in NoSQL state stores for GenAI apps

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Explain the difference between eventual consistency and strong consistency in AWS DynamoDB and Cosmos DB, and write Python code simulating race conditions in eventual consistency.

## Answer

In DynamoDB:
- **Eventually Consistent Reads (default)**: Consumes 0.5 Read Capacity Units (RCUs) per 4 KB. Data is read from one replica, which might not reflect a write that completed milliseconds prior.
- **Strongly Consistent Reads**: Consumes 1.0 RCU per 4 KB. Reads from a quorum of replicas, guaranteeing that the most recent write is returned.

In GenAI chat applications:
If a user submits turn 2 immediately after turn 1, an eventually consistent read might miss turn 1's assistant reply, causing the LLM to hallucinate or repeat itself. Therefore, conversational turn retrieval should use **Strong Consistency**.

```python
import random
from typing import Dict, List, Optional


class MockDynamoDBReplicaStore:
    def __init__(self):
        # 3 replicas simulating a DynamoDB storage node quorum
        self.replicas = [{}, {}, {}]

    def put_item(self, key: str, value: str) -> None:
        # Write committed to quorum (first 2 nodes)
        self.replicas[0][key] = value
        self.replicas[1][key] = value
        # 3rd node has replication lag (eventually updated)

    def get_eventual(self, key: str) -> Optional[str]:
        # Reads from a randomly selected single replica (might hit node 2 which is empty)
        replica = self.replicas[2]  # Simulating lagged replica read
        return replica.get(key)

    def get_strong(self, key: str) -> Optional[str]:
        # Reads from majority quorum (first 2 nodes)
        v0 = self.replicas[0].get(key)
        v1 = self.replicas[1].get(key)
        return v0 if v0 == v1 else None


store = MockDynamoDBReplicaStore()
store.put_item("th_01_last_msg", "Assistant: Execution complete.")

# Eventual read hits lagged node
assert store.get_eventual("th_01_last_msg") is None

# Strong read queries quorum
assert store.get_strong("th_01_last_msg") == "Assistant: Execution complete."
```

## Likely follow-ups

- What is the financial cost implication of enabling strong consistency across millions of daily chat turns?
- How does Cosmos DB Session Consistency provide a middle ground between Strong and Eventual?

---

[← Q0829](../../batch_09_genai_services_fastapi/0829_bulk_export_and_retention_policies_for_compliance_chat/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0831 →](../../batch_09_genai_services_fastapi/0831_redis_vector_similarity_search_for_semantic_prompt_response/README.md)

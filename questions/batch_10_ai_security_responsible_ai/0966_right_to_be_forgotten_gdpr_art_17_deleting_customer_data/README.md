# Q0966 · Right to be Forgotten (GDPR Art. 17): deleting customer data from vector stores

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Write Python code implementing an automated GDPR Article 17 ("Right to be Forgotten") deletion worker that purges all customer embeddings, chat logs, and metadata across vector databases and Redis caches.

## Answer

Under GDPR Article 17, when a customer requests data erasure, the bank must delete all personal data within 30 days. In GenAI platforms, this requires:
1. Purging conversation history from NoSQL state stores (DynamoDB/Cosmos DB).
2. Deleting embeddings and metadata chunks from vector stores.
3. Invalidating cached responses in Redis.

```python
from typing import Dict, List, Set


class GDPRPurgeOrchestrator:
    def __init__(self):
        self.vector_store: Dict[str, List[dict]] = {}  # tenant/user -> chunks
        self.chat_history: Dict[str, List[dict]] = {}  # user -> sessions
        self.redis_cache: Dict[str, str] = {}          # cache_key -> val

    def execute_user_purge(self, user_id: str) -> dict:
        deleted_chats = len(self.chat_history.pop(user_id, []))
        deleted_vectors = len(self.vector_store.pop(user_id, []))

        # Evict cache keys matching user pattern
        cache_keys_to_del = [k for k in self.redis_cache if user_id in k]
        for k in cache_keys_to_del:
            del self.redis_cache[k]

        return {
            "user_id": user_id,
            "status": "PURGED",
            "records_deleted": {
                "chats": deleted_chats,
                "vectors": deleted_vectors,
                "cache_entries": len(cache_keys_to_del),
            },
        }


purge_tool = GDPRPurgeOrchestrator()
purge_tool.chat_history["user_99"] = [{"msg": "Hello"}, {"msg": "Balance"}]
purge_tool.vector_store["user_99"] = [{"id": "v1"}, {"id": "v2"}, {"id": "v3"}]
purge_tool.redis_cache["session:user_99:cache"] = "cached response"

report = purge_tool.execute_user_purge("user_99")
assert report["status"] == "PURGED"
assert report["records_deleted"]["chats"] == 2
assert report["records_deleted"]["vectors"] == 3
assert report["records_deleted"]["cache_entries"] == 1
assert "user_99" not in purge_tool.chat_history
```

## Likely follow-ups

- What happens if customer data was baked into model weights during fine-tuning? (Machine Unlearning).
- Why is re-indexing vector databases required after bulk GDPR deletions?

---

[← Q0965](../../batch_10_ai_security_responsible_ai/0965_model_inversion_attacks_reconstructing_private_inputs_from/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0967 →](../../batch_10_ai_security_responsible_ai/0967_detecting_internal_financial_insider_information_mnpi_in/README.md)

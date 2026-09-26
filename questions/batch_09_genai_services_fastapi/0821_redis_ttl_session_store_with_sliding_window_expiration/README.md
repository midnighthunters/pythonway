# Q0821 · Redis TTL session store with sliding window expiration

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Easy |

## Question

Write Python code using an in-memory mock or dictionary simulation of a Redis session store for chat conversations, implementing TTL expiration, message appending, and sliding-window TTL refresh on every user interaction.

## Answer

In enterprise chat applications, short-term conversational context is maintained in Redis to enable ultra-fast retrieval during multi-turn LLM inference. A sliding-window TTL ensures that active sessions remain available while idle sessions expire cleanly, freeing Redis memory.

```python
import time
from typing import Any, Dict, List, Optional


class RedisSessionStore:
    def __init__(self, default_ttl_seconds: int = 1800):
        self.default_ttl = default_ttl_seconds
        # Mapping: session_id -> {"expires_at": float, "messages": list}
        self.store: Dict[str, Dict[str, Any]] = {}

    def _purge_if_expired(self, session_id: str) -> None:
        if session_id in self.store:
            if time.time() > self.store[session_id]["expires_at"]:
                del self.store[session_id]

    def append_message(self, session_id: str, role: str, content: str) -> None:
        self._purge_if_expired(session_id)
        now = time.time()
        if session_id not in self.store:
            self.store[session_id] = {
                "expires_at": now + self.default_ttl,
                "messages": [],
            }
        else:
            # Refresh sliding window TTL
            self.store[session_id]["expires_at"] = now + self.default_ttl
        self.store[session_id]["messages"].append({"role": role, "content": content})

    def get_messages(self, session_id: str) -> List[Dict[str, str]]:
        self._purge_if_expired(session_id)
        if session_id not in self.store:
            return []
        return list(self.store[session_id]["messages"])


store = RedisSessionStore(default_ttl_seconds=10)
store.append_message("sess_101", "user", "Hello market risk desk")
store.append_message("sess_101", "assistant", "Hello! How can I assist with VaR today?")

msgs = store.get_messages("sess_101")
assert len(msgs) == 2
assert msgs[0]["role"] == "user"

# Artificially expire the session
store.store["sess_101"]["expires_at"] = time.time() - 1
assert store.get_messages("sess_101") == []
```

## Likely follow-ups

- How does Redis `EXPIRE` command differ from an active memory eviction policy like `volatile-lru`?
- How do you handle session migration when Redis nodes restart?

---

[← Q0820](../../batch_09_genai_services_fastapi/0820_optimistic_concurrency_control_for_parallel_agent_state/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0822 →](../../batch_09_genai_services_fastapi/0822_cosmos_db_partition_key_strategies_for_enterprise_chat_apps/README.md)

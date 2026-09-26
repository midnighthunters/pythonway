# Q0537 · Long-term memory with the Store

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Memory | Medium |

## Question

Use LangGraph's `Store` to keep long-term memories per user across threads, organised by namespace, and read them back.

## Answer

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
store.put(("memories", "u-priya"), "seat", {"text": "Prefers aisle seats", "source": "chat 2026-09-20"})
store.put(("memories", "u-priya"), "office", {"text": "Works from Canary Wharf"})
store.put(("memories", "u-tom"), "diet", {"text": "Vegetarian"})

assert store.get(("memories", "u-priya"), "seat").value["text"] == "Prefers aisle seats"
priya = sorted(item.key for item in store.search(("memories", "u-priya")))
assert priya == ["office", "seat"]
assert [i.key for i in store.search(("memories", "u-tom"))] == ["diet"]
store.delete(("memories", "u-priya"), "seat")
assert store.get(("memories", "u-priya"), "seat") is None
```

Checkpointers hold per-thread state (one conversation or run). The Store holds cross-thread data (preferences, facts, episodic lessons), keyed by namespace tuples such as `("memories", user_id)`. In production, use a persistent store (for example Postgres), derive namespaces from the authenticated identity (never from model output), support user-driven deletion, and record provenance in each item.

## Likely follow-ups

- Why must the namespace come from the authenticated identity?

---

[← Q0536](../../batch_06_langgraph_langchain/0536_runtime_context_with_context_schema/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0538 →](../../batch_06_langgraph_langchain/0538_semantic_search_in_the_store/README.md)

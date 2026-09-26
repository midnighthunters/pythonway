# Q0538 · Semantic search in the Store

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Memory | Medium |

## Question

Configure the Store with an embedding function, so memories can be retrieved by meaning (for example "seat preference") rather than exact key.

## Answer

```python
from langgraph.store.memory import InMemoryStore

VOCAB = ["aisle", "window", "seat", "vegan", "vegetarian", "office", "wharf"]


def embed(texts: list[str]) -> list[list[float]]:
    return [[float(w in t.lower()) for w in VOCAB] for t in texts]


store = InMemoryStore(index={"dims": len(VOCAB), "embed": embed})
ns = ("memories", "u-priya")
store.put(ns, "m1", {"text": "Prefers aisle seat on long flights"})
store.put(ns, "m2", {"text": "Vegan meals only"})
store.put(ns, "m3", {"text": "Office is Canary Wharf"})
hits = store.search(ns, query="which seat does she like?", limit=1)
assert hits[0].key == "m1" and hits[0].score > 0
assert store.search(ns, query="where is her office in the wharf", limit=1)[0].key == "m3"
```

The toy embedding stands in for a real embedding model. Semantic retrieval lets the agent pull only the relevant memories into the context each turn, instead of dumping everything. Scope searches to the user's namespace, set a relevance threshold, and remember that retrieved memories are hints (they can be stale), so the agent should confirm important ones.

## Likely follow-ups

- How many memories would you inject per turn, and how would you choose?

---

[← Q0537](../../batch_06_langgraph_langchain/0537_long_term_memory_with_the_store/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0539 →](../../batch_06_langgraph_langchain/0539_use_the_store_inside_nodes/README.md)

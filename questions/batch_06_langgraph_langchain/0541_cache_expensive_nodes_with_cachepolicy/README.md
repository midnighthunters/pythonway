# Q0541 · Cache expensive nodes with CachePolicy

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Performance | Medium |

## Question

Cache the result of an expensive, deterministic node (for example a policy lookup), so repeated inputs within a TTL skip the work.

## Answer

```python
from typing import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.graph import END, START, StateGraph
from langgraph.types import CachePolicy

lookups = {"n": 0}


class State(TypedDict):
    city: str
    cap: str


def policy_lookup(state: State) -> dict:
    lookups["n"] += 1
    return {"cap": {"London": "180 GBP", "Paris": "160 EUR"}[state["city"]]}


b = StateGraph(State)
b.add_node("policy_lookup", policy_lookup, cache_policy=CachePolicy(ttl=300))
b.add_edge(START, "policy_lookup")
b.add_edge("policy_lookup", END)
g = b.compile(cache=InMemoryCache())
assert g.invoke({"city": "London", "cap": ""})["cap"] == "180 GBP"
assert g.invoke({"city": "London", "cap": ""})["cap"] == "180 GBP"
assert g.invoke({"city": "Paris", "cap": ""})["cap"] == "160 EUR"
assert lookups["n"] == 2
```

The cache key is derived from the node's input by default (a custom `key_func` can narrow it). Only cache pure, deterministic nodes. Never cache per-user or entitlement-dependent results unless the user or scope is part of the key. Use a shared cache backend across replicas in production.

## Likely follow-ups

- Why is caching a node that reads the current balance a bad idea?

---

[← Q0540](../../batch_06_langgraph_langchain/0540_retry_policies_on_nodes/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0542 →](../../batch_06_langgraph_langchain/0542_durability_modes/README.md)

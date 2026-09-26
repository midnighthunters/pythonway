# Q0539 · Use the store inside nodes

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Memory | Medium |

## Question

Write nodes that save and recall memories through `runtime.store`, namespaced by the user id from the runtime context, and show that users are isolated.

## Answer

```python
from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.store.memory import InMemoryStore


@dataclass
class Ctx:
    user_id: str


class State(TypedDict):
    remember: str
    recalled: list[str]


def save(state: State, runtime: Runtime[Ctx]) -> dict:
    if state["remember"]:
        ns = ("memories", runtime.context.user_id)
        key = f"m{len(runtime.store.search(ns)) + 1}"
        runtime.store.put(ns, key, {"text": state["remember"]})
    return {}


def recall(state: State, runtime: Runtime[Ctx]) -> dict:
    items = runtime.store.search(("memories", runtime.context.user_id))
    return {"recalled": sorted(i.value["text"] for i in items)}


b = StateGraph(State, context_schema=Ctx)
b.add_node("save", save)
b.add_node("recall", recall)
b.add_edge(START, "save")
b.add_edge("save", "recall")
b.add_edge("recall", END)
g = b.compile(store=InMemoryStore())
g.invoke({"remember": "aisle seat", "recalled": []}, context=Ctx("u-priya"))
out = g.invoke({"remember": "Canary Wharf office", "recalled": []}, context=Ctx("u-priya"))
assert out["recalled"] == ["Canary Wharf office", "aisle seat"]
assert g.invoke({"remember": "", "recalled": []}, context=Ctx("u-tom"))["recalled"] == []
```

Only save memories from the user's own statements, never from documents or tool output (memory poisoning). Show the user what was remembered. Reading and writing through the runtime keeps nodes testable, because you inject a different store in tests.

## Likely follow-ups

- How would you let a user list and delete their memories?

---

[← Q0538](../../batch_06_langgraph_langchain/0538_semantic_search_in_the_store/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0540 →](../../batch_06_langgraph_langchain/0540_retry_policies_on_nodes/README.md)

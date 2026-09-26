# Q0504 · Your first StateGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Easy |

## Question

Build a two-node LangGraph workflow that normalises a user question and then classifies it, and show its output.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    normalized: str
    category: str


def normalize(state: State) -> dict:
    return {"normalized": " ".join(state["question"].lower().split())}


def classify(state: State) -> dict:
    text = state["normalized"]
    return {"category": "travel" if "hotel" in text or "flight" in text else "other"}


builder = StateGraph(State)
builder.add_node("normalize", normalize)
builder.add_node("classify", classify)
builder.add_edge(START, "normalize")
builder.add_edge("normalize", "classify")
builder.add_edge("classify", END)
graph = builder.compile()

out = graph.invoke({"question": "  What is the HOTEL cap in London? "})
assert out == {"question": "  What is the HOTEL cap in London? ", "normalized": "what is the hotel cap in london?",
               "category": "travel"}
```

Nodes return only the keys they change, and LangGraph merges them into the state. `compile()` validates the graph structure (missing nodes, dangling edges) and returns a runnable with `invoke`, `stream`, `batch` and their async variants.

## Likely follow-ups

- What does `compile()` check, and what can't it check?

---

[← Q0503](../../batch_06_langgraph_langchain/0503_state_nodes_and_edges/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0505 →](../../batch_06_langgraph_langchain/0505_reducers_and_state_channels/README.md)

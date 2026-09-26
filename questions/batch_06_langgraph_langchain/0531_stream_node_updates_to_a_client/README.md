# Q0531 · Stream node updates to a client

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Streaming | Easy |

## Question

Stream node-level updates from a graph and turn them into user-facing progress events.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    docs: list[str]
    answer: str


b = StateGraph(State)
b.add_node("retrieve", lambda s: {"docs": ["pol-7", "faq-2"]})
b.add_node("generate", lambda s: {"answer": f"Based on {len(s['docs'])} sources..."})
b.add_edge(START, "retrieve")
b.add_edge("retrieve", "generate")
b.add_edge("generate", END)

LABELS = {"retrieve": lambda u: f"Found {len(u['docs'])} relevant documents",
          "generate": lambda u: "Answer ready"}
events = []
for chunk in b.compile().stream({"docs": [], "answer": ""}, stream_mode="updates"):
    for node, update in chunk.items():
        events.append({"event": "progress", "text": LABELS[node](update)})
assert events == [{"event": "progress", "text": "Found 2 relevant documents"},
                  {"event": "progress", "text": "Answer ready"}]
```

Each chunk maps a node name to the update it returned. Map these to user-safe labels rather than forwarding raw updates, which may contain internal content (document text, scores, tool payloads).

## Likely follow-ups

- How would you stream this over SSE from FastAPI?

---

[← Q0530](../../batch_06_langgraph_langchain/0530_streaming_modes_overview/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0532 →](../../batch_06_langgraph_langchain/0532_stream_llm_tokens_with_messages_mode/README.md)

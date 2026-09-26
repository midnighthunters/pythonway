# Q0533 · Custom progress events with get_stream_writer

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Streaming | Medium |

## Question

A node runs a long reconciliation job. Emit custom progress events from inside the node with `get_stream_writer()`, and consume them together with node updates.

## Answer

```python
from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    matched: int


def reconcile(state: State) -> dict:
    write = get_stream_writer()
    total, matched = 4, 0
    for i in range(1, total + 1):
        matched += 1
        write({"progress": round(i / total, 2), "message": f"matched batch {i}/{total}"})
    return {"matched": matched}


b = StateGraph(State)
b.add_node("reconcile", reconcile)
b.add_edge(START, "reconcile")
b.add_edge("reconcile", END)
seen = list(b.compile().stream({"matched": 0}, stream_mode=["custom", "updates"]))
customs = [c for mode, c in seen if mode == "custom"]
updates = [c for mode, c in seen if mode == "updates"]
assert [c["progress"] for c in customs] == [0.25, 0.5, 0.75, 1.0]
assert updates == [{"reconcile": {"matched": 4}}]
```

With several modes, the stream yields `(mode, chunk)` tuples. Custom events are ideal for long tools (progress bars, "waiting for supplier API"), and they aren't persisted in the state, so they don't bloat checkpoints.

## Likely follow-ups

- Should progress events be persisted anywhere?

---

[← Q0532](../../batch_06_langgraph_langchain/0532_stream_llm_tokens_with_messages_mode/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0534 →](../../batch_06_langgraph_langchain/0534_subgraphs_as_nodes/README.md)

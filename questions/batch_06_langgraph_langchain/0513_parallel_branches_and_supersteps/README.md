# Q0513 · Parallel branches and supersteps

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Run two independent nodes in parallel from `START`, join them, and show what happens when parallel nodes write the same non-reducer key.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.errors import InvalidUpdateError
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    results: Annotated[list[str], operator.add]
    status: str


def flights(state: State) -> dict:
    return {"results": ["flights:3 options"]}


def hotels(state: State) -> dict:
    return {"results": ["hotels:5 options"]}


b = StateGraph(State)
b.add_node("flights", flights)
b.add_node("hotels", hotels)
b.add_node("combine", lambda s: {"status": f"{len(s['results'])} sources ready"})
b.add_edge(START, "flights")
b.add_edge(START, "hotels")
b.add_edge(["flights", "hotels"], "combine")
b.add_edge("combine", END)
out = b.compile().invoke({"results": [], "status": ""})
assert sorted(out["results"]) == ["flights:3 options", "hotels:5 options"] and out["status"] == "2 sources ready"

clash = StateGraph(State)
clash.add_node("a", lambda s: {"status": "from a"})
clash.add_node("b", lambda s: {"status": "from b"})
clash.add_edge(START, "a")
clash.add_edge(START, "b")
clash.add_edge("a", END)
clash.add_edge("b", END)
try:
    clash.compile().invoke({"results": [], "status": ""})
    raise AssertionError("expected a conflict")
except InvalidUpdateError:
    pass
```

Nodes in the same superstep run concurrently, and their updates are applied together at the end of the step. Two writes to a key without a reducer are ambiguous, so LangGraph raises `InvalidUpdateError` rather than silently picking one. If a parallel branch fails, the whole superstep fails (updates are transactional per step). Combine this with retry policies.

## Likely follow-ups

- Why is the whole superstep rolled back when one branch fails?

---

[← Q0512](../../batch_06_langgraph_langchain/0512_map_reduce_fan_out_with_send/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0514 →](../../batch_06_langgraph_langchain/0514_input_and_output_schemas/README.md)

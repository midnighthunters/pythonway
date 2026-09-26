# Q0527 · Inspect state snapshots

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Persistence | Medium |

## Question

Use `get_state` to inspect a thread's current values, the next nodes to run, and its checkpoint metadata, for example to power a "run status" API.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt


class State(TypedDict):
    steps: Annotated[list[str], operator.add]


b = StateGraph(State)
b.add_node("search", lambda s: {"steps": ["search"]})
b.add_node("confirm", lambda s: {"steps": [f"confirm:{interrupt('Book LH903?')}"]})
b.add_edge(START, "search")
b.add_edge("search", "confirm")
b.add_edge("confirm", END)
app = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "trip-42"}}
app.invoke({"steps": []}, cfg)

snap = app.get_state(cfg)
status = {
    "values": snap.values,
    "waiting_on": list(snap.next),
    "pending_question": snap.tasks[0].interrupts[0].value if snap.tasks and snap.tasks[0].interrupts else None,
    "checkpoint_id": snap.config["configurable"]["checkpoint_id"],
}
assert status["values"] == {"steps": ["search"]} and status["waiting_on"] == ["confirm"]
assert status["pending_question"] == "Book LH903?" and status["checkpoint_id"]
```

A status endpoint built on `get_state` lets the UI show "waiting for your confirmation" after a page reload or on another device. Filter what you expose: the full state may contain internal data that users shouldn't see.

## Likely follow-ups

- How would you list all threads waiting for approval for a given approver?

---

[← Q0526](../../batch_06_langgraph_langchain/0526_static_breakpoints_with_interrupt_before/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0528 →](../../batch_06_langgraph_langchain/0528_time_travel_replay_and_fork/README.md)

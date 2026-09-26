# Q0529 · Correct an agent with update_state

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Human-in-the-loop | Medium |

## Question

An agent paused before a booking step has picked the wrong flight. Use `update_state` to correct the value, then let the run continue.

## Answer

```python
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    chosen_flight: str
    booked: str


b = StateGraph(State)
b.add_node("choose", lambda s: {"chosen_flight": "BA912"})
b.add_node("book", lambda s: {"booked": f"ticket for {s['chosen_flight']}"})
b.add_edge(START, "choose")
b.add_edge("choose", "book")
b.add_edge("book", END)
app = b.compile(checkpointer=InMemorySaver(), interrupt_before=["book"])
cfg = {"configurable": {"thread_id": "rebook-7"}}

assert app.invoke({"chosen_flight": "", "booked": ""}, cfg)["chosen_flight"] == "BA912"
app.update_state(cfg, {"chosen_flight": "LH903"})
assert app.invoke(None, cfg) == {"chosen_flight": "LH903", "booked": "ticket for LH903"}
```

`chosen_flight` has no reducer, so the update overwrites it. This "edit state, then continue" pattern is how a reviewer fixes an agent's choice without re-running the expensive earlier steps. Record who edited what (the update is itself a checkpoint), and validate the edited values as strictly as model output.

## Likely follow-ups

- How would you record the reviewer's identity with the edit?

---

[← Q0528](../../batch_06_langgraph_langchain/0528_time_travel_replay_and_fork/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0530 →](../../batch_06_langgraph_langchain/0530_streaming_modes_overview/README.md)

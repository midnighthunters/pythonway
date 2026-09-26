# Q0526 · Static breakpoints with interrupt_before

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Human-in-the-loop | Medium |

## Question

Use `interrupt_before` at compile time to pause before a node for debugging or review, then continue the run.

## Answer

```python
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    draft: str
    sent: bool


b = StateGraph(State)
b.add_node("draft_email", lambda s: {"draft": "Hi Tom, the agenda is attached."})
b.add_node("send_email", lambda s: {"sent": True})
b.add_edge(START, "draft_email")
b.add_edge("draft_email", "send_email")
b.add_edge("send_email", END)
app = b.compile(checkpointer=InMemorySaver(), interrupt_before=["send_email"])
cfg = {"configurable": {"thread_id": "dbg-1"}}

paused = app.invoke({"draft": "", "sent": False}, cfg)
assert paused == {"draft": "Hi Tom, the agenda is attached.", "sent": False}
assert app.get_state(cfg).next == ("send_email",)
assert app.invoke(None, cfg)["sent"] is True
```

Invoking with `None` continues from the paused checkpoint. Static breakpoints (`interrupt_before` and `interrupt_after`) are handy for debugging and simple review steps, but they're configured per node for all runs. Dynamic `interrupt()` inside a node is more flexible for real approval logic (pause only for large amounts, with a custom payload).

## Likely follow-ups

- When would you prefer a dynamic interrupt to a static breakpoint?

---

[← Q0525](../../batch_06_langgraph_langchain/0525_validate_human_input_in_an_interrupt_loop/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0527 →](../../batch_06_langgraph_langchain/0527_inspect_state_snapshots/README.md)

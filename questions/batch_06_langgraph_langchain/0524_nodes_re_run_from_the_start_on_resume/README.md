# Q0524 · Nodes re-run from the start on resume

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Human-in-the-loop | Hard |

## Question

When a graph resumes after an interrupt, the interrupted node runs again from its first line. Demonstrate this with a side-effect counter and two sequential approval nodes, and explain how to write interrupt-safe nodes.

## Answer

```python
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

calls = {"before_interrupt": 0}


class State(TypedDict):
    amount_ok: bool
    recipient_ok: bool


def approve_amount(state: State) -> dict:
    calls["before_interrupt"] += 1
    return {"amount_ok": interrupt("Approve amount 950 GBP?") == "yes"}


def approve_recipient(state: State) -> dict:
    return {"recipient_ok": interrupt("Approve new recipient ACME Ltd?") == "yes"}


b = StateGraph(State)
b.add_node("approve_amount", approve_amount)
b.add_node("approve_recipient", approve_recipient)
b.add_edge(START, "approve_amount")
b.add_edge("approve_amount", "approve_recipient")
b.add_edge("approve_recipient", END)
app = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "t-1"}}

assert app.invoke({"amount_ok": False, "recipient_ok": False}, cfg)["__interrupt__"][0].value.startswith("Approve amount")
second = app.invoke(Command(resume="yes"), cfg)
assert second["__interrupt__"][0].value.startswith("Approve new recipient")
final = app.invoke(Command(resume="yes"), cfg)
assert final == {"amount_ok": True, "recipient_ok": True}
assert calls["before_interrupt"] == 2
```

The code before `interrupt()` ran twice: once before the pause and again on resume. Rules for interrupt-safe nodes:
- Put side effects after the interrupt, or in a separate node after approval.
- Make any pre-interrupt work idempotent, or cheap and read-only.
- Keep the order of multiple `interrupt()` calls within a node deterministic, because resume values are matched by position.

## Likely follow-ups

- What would happen if the pre-interrupt code sent an email?

---

[← Q0523](../../batch_06_langgraph_langchain/0523_approval_with_interrupt/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0525 →](../../batch_06_langgraph_langchain/0525_validate_human_input_in_an_interrupt_loop/README.md)

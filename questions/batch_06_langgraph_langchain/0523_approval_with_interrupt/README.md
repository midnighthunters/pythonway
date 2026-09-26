# Q0523 · Approval with interrupt()

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Human-in-the-loop | Medium |

## Question

Pause a graph for human approval of a payment with `interrupt()`, inspect the pending interrupt, and resume with the reviewer's decision.

## Answer

```python
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    invoice_id: str
    amount: float
    status: str


def approval(state: State) -> dict:
    decision = interrupt({"question": "Release this payment?", "invoice_id": state["invoice_id"], "amount": state["amount"]})
    return {"status": "released" if decision == "approve" else "held"}


b = StateGraph(State)
b.add_node("approval", approval)
b.add_edge(START, "approval")
b.add_edge("approval", END)
app = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "pay-INV-7"}}

paused = app.invoke({"invoice_id": "INV-7", "amount": 950.0, "status": "pending"}, cfg)
assert paused["__interrupt__"][0].value["amount"] == 950.0
snapshot = app.get_state(cfg)
assert snapshot.next == ("approval",) and snapshot.tasks[0].interrupts[0].value["invoice_id"] == "INV-7"
assert app.invoke(Command(resume="approve"), cfg)["status"] == "released"
```

The interrupt value (any JSON-serialisable payload) is surfaced to the caller and persisted with the checkpoint, and the run can wait indefinitely. `Command(resume=...)` supplies the value that `interrupt()` returns when the node re-runs. Authenticate the resume call and check that the approver is allowed to decide (four-eyes), because resuming is itself a privileged action.

## Likely follow-ups

- Where would you enforce that the approver isn't the requester?

---

[← Q0522](../../batch_06_langgraph_langchain/0522_choosing_a_production_checkpointer/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0524 →](../../batch_06_langgraph_langchain/0524_nodes_re_run_from_the_start_on_resume/README.md)

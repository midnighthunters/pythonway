# Q0594 · Side effects and replays in LangGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Reliability | Hard |

## Question

Nodes can re-run (resume after an interrupt, retries, forks). Show how an idempotency key derived from the thread id makes a payment node safe even though the node executes twice.

## Answer

```python
from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

LEDGER: dict[str, dict] = {}
payment_api_calls = {"n": 0}


def pay_once(idempotency_key: str, amount: float) -> dict:
    if idempotency_key in LEDGER:
        return LEDGER[idempotency_key]
    payment_api_calls["n"] += 1
    LEDGER[idempotency_key] = {"payment_id": f"PAY-{len(LEDGER) + 1}", "amount": amount}
    return LEDGER[idempotency_key]


class State(TypedDict):
    amount: float
    payment_id: str
    confirmed: bool


def pay_and_confirm(state: State, config: RunnableConfig) -> dict:
    key = f"{config['configurable']['thread_id']}:pay_and_confirm"
    receipt = pay_once(key, state["amount"])
    confirmed = interrupt({"question": "Did the supplier confirm receipt?", "payment_id": receipt["payment_id"]})
    return {"payment_id": receipt["payment_id"], "confirmed": bool(confirmed)}


b = StateGraph(State)
b.add_node("pay_and_confirm", pay_and_confirm)
b.add_edge(START, "pay_and_confirm")
b.add_edge("pay_and_confirm", END)
app = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "po-991"}}
app.invoke({"amount": 250.0, "payment_id": "", "confirmed": False}, cfg)
out = app.invoke(Command(resume=True), cfg)
assert out == {"amount": 250.0, "payment_id": "PAY-1", "confirmed": True}
assert payment_api_calls["n"] == 1 and len(LEDGER) == 1
```

The node ran twice (before the interrupt and again on resume), but the payment happened once. The better design is still to move side effects after the interrupt, or into their own node (or into a `@task` in the functional API). Idempotency keys are the backstop, and downstream payment APIs should enforce them too. Include the checkpoint or fork id in the key if forks should legitimately create new payments.

## Likely follow-ups

- Should a forked run reuse the original payment's idempotency key?

---

[← Q0593](../../batch_06_langgraph_langchain/0593_debugging_a_stuck_or_looping_graph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0595 →](../../batch_06_langgraph_langchain/0595_human_in_the_loop_ux_with_langgraph/README.md)

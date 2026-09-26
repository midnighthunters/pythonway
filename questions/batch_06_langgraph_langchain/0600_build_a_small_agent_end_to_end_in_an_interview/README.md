# Q0600 · Build a small agent end to end in an interview

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph implementation | Hard |

## Question

In 30 minutes, build a LangGraph assistant that routes policy questions to a retrieval node and refund requests to a tool agent with human approval, uses a checkpointer, and prove the trajectories with streamed updates.

## Answer

```python
from typing import Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

POLICIES = {"hotel": "[pol-7] London hotels are capped at 180 GBP per night."}
REFUNDS: list[str] = []


class State(TypedDict):
    request: str
    route: str
    answer: str


def router(s: State) -> dict:
    return {"route": "refund" if "refund" in s["request"].lower() else "policy"}


def policy_qa(s: State) -> dict:
    hits = [v for k, v in POLICIES.items() if k in s["request"].lower()]
    return {"answer": hits[0] if hits else "I couldn't find this in the policies."}


def refund_agent(s: State) -> Command[Literal["execute_refund", "__end__"]]:
    invoice = next((w.strip("?.,") for w in s["request"].split() if w.upper().startswith("INV-")), None)
    if invoice is None:
        return Command(goto=END, update={"answer": "Which invoice should I refund?"})
    decision = interrupt({"action": "issue_refund", "invoice": invoice})
    if decision != "approve":
        return Command(goto=END, update={"answer": f"Refund for {invoice} was not approved."})
    return Command(goto="execute_refund", update={"answer": invoice})


def execute_refund(s: State) -> dict:
    REFUNDS.append(s["answer"])
    return {"answer": f"Refund issued for {s['answer']}."}


b = StateGraph(State)
b.add_node("router", router)
b.add_node("policy_qa", policy_qa)
b.add_node("refund_agent", refund_agent)
b.add_node("execute_refund", execute_refund)
b.add_edge(START, "router")
b.add_conditional_edges("router", lambda s: "refund_agent" if s["route"] == "refund" else "policy_qa",
                        ["refund_agent", "policy_qa"])
b.add_edge("policy_qa", END)
b.add_edge("execute_refund", END)
app = b.compile(checkpointer=InMemorySaver())


def run(inputs, thread: str) -> list[str]:
    cfg = {"configurable": {"thread_id": thread}}
    return [node for chunk in app.stream(inputs, cfg, stream_mode="updates") for node in chunk]


assert run({"request": "What is the hotel cap?", "route": "", "answer": ""}, "t1") == ["router", "policy_qa"]
assert run({"request": "Please refund INV-0042", "route": "", "answer": ""}, "t2") == ["router", "__interrupt__"]
assert REFUNDS == []
assert run(Command(resume="approve"), "t2") == ["refund_agent", "execute_refund"]
assert REFUNDS == ["INV-0042"]
assert app.get_state({"configurable": {"thread_id": "t2"}}).values["answer"] == "Refund issued for INV-0042."
```

The interview checklist this covers: typed state, deterministic routing, a retrieval stub, a human approval with `interrupt()` before any side effect, durable threads via a checkpointer, and trajectory assertions from `stream_mode="updates"` (where the interrupt appears as an `__interrupt__` entry). Then talk through what you'd add: real retrieval and models, idempotency on refunds, entitlement checks, evaluations and tracing.

## Likely follow-ups

- What would you add first to make this production-ready?
- How would you test the reject path?

---

[← Q0599](../../batch_06_langgraph_langchain/0599_rebooking_workflow_as_a_langgraph_graph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md)

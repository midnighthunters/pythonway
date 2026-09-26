# Q0511 · Update and route with Command

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Show how a node can both update the state and choose the next node by returning `Command(update=..., goto=...)`, and when that's preferable to a conditional edge.

## Answer

```python
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


class State(TypedDict):
    amount: float
    decision: str


def triage(state: State) -> Command[Literal["auto_approve", "manual_review"]]:
    if state["amount"] <= 100:
        return Command(update={"decision": "auto"}, goto="auto_approve")
    return Command(update={"decision": "review"}, goto="manual_review")


b = StateGraph(State)
b.add_node("triage", triage)
b.add_node("auto_approve", lambda s: {"decision": s["decision"] + ":approved"})
b.add_node("manual_review", lambda s: {"decision": s["decision"] + ":queued"})
b.add_edge(START, "triage")
b.add_edge("auto_approve", END)
b.add_edge("manual_review", END)
g = b.compile()
assert g.invoke({"amount": 40.0, "decision": ""})["decision"] == "auto:approved"
assert g.invoke({"amount": 900.0, "decision": ""})["decision"] == "review:queued"
```

Use `Command` when the routing decision and the state update come from the same logic (for example an LLM decision that also records its reasoning), and for multi-agent handoffs (including `graph=Command.PARENT` to route in a parent graph from a subgraph). The `Command[Literal[...]]` return annotation documents the possible destinations for validation and graph drawing. Use conditional edges when routing is a pure function of the state.

## Likely follow-ups

- How does a subgraph node hand off to a node in its parent graph?

---

[← Q0510](../../batch_06_langgraph_langchain/0510_loops_and_the_recursion_limit/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0512 →](../../batch_06_langgraph_langchain/0512_map_reduce_fan_out_with_send/README.md)

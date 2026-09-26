# Q0547 · Handoffs between agents with Command

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Multi-agent | Medium |

## Question

Implement a network of agents (triage, billing and technical support) where the active agent hands off to another by returning `Command(goto=...)` with a handoff message, and where ping-pong handoffs are capped.

## Answer

```python
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.types import Command

MAX_HANDOFFS = 3


def count_handoffs(state: MessagesState) -> int:
    return sum(1 for m in state["messages"] if m.content.startswith("[handoff"))


def triage(state: MessagesState) -> Command[Literal["billing", "tech", "__end__"]]:
    text = state["messages"][0].content.lower()
    target = "billing" if "invoice" in text else "tech" if "login" in text else None
    if target is None:
        return Command(goto="__end__", update={"messages": [AIMessage("How can I help?")]})
    return Command(goto=target, update={"messages": [AIMessage(f"[handoff triage->{target}] {text[:30]}")]})


def billing(state: MessagesState) -> Command[Literal["tech", "__end__"]]:
    if "login" in state["messages"][0].content.lower() and count_handoffs(state) < MAX_HANDOFFS:
        return Command(goto="tech", update={"messages": [AIMessage("[handoff billing->tech] login part")]})
    return Command(goto="__end__", update={"messages": [AIMessage("Billing: your invoice was re-sent.")]})


def tech(state: MessagesState) -> Command[Literal["__end__"]]:
    return Command(goto="__end__", update={"messages": [AIMessage("Tech: your login was reset.")]})


b = StateGraph(MessagesState)
for name, fn in (("triage", triage), ("billing", billing), ("tech", tech)):
    b.add_node(name, fn)
b.add_edge(START, "triage")
g = b.compile()
out = g.invoke({"messages": [HumanMessage("I can't login to see my invoice")]})
assert [m.content.split("]")[0] for m in out["messages"][1:3]] == ["[handoff triage->billing", "[handoff billing->tech"]
assert out["messages"][-1].content == "Tech: your login was reset."
```

Handoff messages keep a visible trail of who handled what. In the prebuilt ecosystem, handoffs are often exposed to the model as tools ("transfer_to_billing") that return a `Command`, and inside subgraphs a `Command(graph=Command.PARENT)` routes in the parent graph.

## Likely follow-ups

- What context should travel with a handoff so the user isn't asked to repeat themselves?

---

[← Q0546](../../batch_06_langgraph_langchain/0546_supervisor_pattern_in_langgraph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0548 →](../../batch_06_langgraph_langchain/0548_plan_and_execute_in_langgraph/README.md)

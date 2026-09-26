# Q0517 · Custom routing after the model

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Agents | Hard |

## Question

Replace `tools_condition` with a custom router: read tools go straight to execution, a sensitive tool goes to a human-review node that uses `interrupt()`, and a rejection is fed back to the model as a tool message.

## Answer

```python
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt

SENSITIVE = {"issue_refund"}


@tool
def issue_refund(invoice_id: str, amount: float) -> str:
    """Refund an invoice."""
    return f"refunded {amount} on {invoice_id}"


replies = iter([
    AIMessage(content="", tool_calls=[{"name": "issue_refund", "args": {"invoice_id": "INV-7", "amount": 450.0}, "id": "c1"}]),
    AIMessage(content="I couldn't issue the refund: it was rejected by the reviewer."),
])


def agent(state: MessagesState) -> dict:
    return {"messages": [next(replies)]}


def route(state: MessagesState) -> Literal["tools", "human_review", "__end__"]:
    last = state["messages"][-1]
    if not getattr(last, "tool_calls", None):
        return END
    return "human_review" if any(tc["name"] in SENSITIVE for tc in last.tool_calls) else "tools"


def human_review(state: MessagesState) -> Command[Literal["tools", "agent"]]:
    call = state["messages"][-1].tool_calls[0]
    decision = interrupt({"tool": call["name"], "args": call["args"]})
    if decision.get("approved"):
        return Command(goto="tools")
    msg = ToolMessage(content=f"Rejected by reviewer: {decision.get('reason', '')}", tool_call_id=call["id"])
    return Command(goto="agent", update={"messages": [msg]})


b = StateGraph(MessagesState)
b.add_node("agent", agent)
b.add_node("tools", ToolNode([issue_refund]))
b.add_node("human_review", human_review)
b.add_edge(START, "agent")
b.add_conditional_edges("agent", route, ["tools", "human_review", END])
b.add_edge("tools", "agent")
g = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "refund-1"}}
first = g.invoke({"messages": [HumanMessage("Refund INV-7")]}, cfg)
assert first["__interrupt__"][0].value == {"tool": "issue_refund", "args": {"invoice_id": "INV-7", "amount": 450.0}}
final = g.invoke(Command(resume={"approved": False, "reason": "duplicate claim"}), cfg)
assert final["messages"][-2].content == "Rejected by reviewer: duplicate claim"
assert final["messages"][-1].content.startswith("I couldn't issue the refund")
```

The rejection becomes a `ToolMessage` answering the pending tool call, so the conversation stays valid for the provider and the model can explain the outcome. A checkpointer is required for interrupts, and the thread id identifies the paused run.

## Likely follow-ups

- How would you handle an AI message that contains both a read call and a sensitive call?

---

[← Q0516](../../batch_06_langgraph_langchain/0516_a_react_agent_graph_with_toolnode/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0518 →](../../batch_06_langgraph_langchain/0518_create_agent_in_langchain_1_x/README.md)

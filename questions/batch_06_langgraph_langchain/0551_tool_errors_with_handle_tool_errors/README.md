# Q0551 · Tool errors with handle_tool_errors

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Agents | Medium |

## Question

Show `ToolNode(handle_tool_errors=True)` turning a tool exception into an error `ToolMessage`, so the model can correct its arguments on the next turn.

## Answer

```python
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def get_balance(account_id: str) -> str:
    """Get the balance for an account id like ACC-0001."""
    if not account_id.startswith("ACC-"):
        raise ValueError(f"invalid account id {account_id!r}; expected ACC-NNNN")
    return "1,200.00 GBP"


replies = iter([
    AIMessage(content="", tool_calls=[{"name": "get_balance", "args": {"account_id": "0001"}, "id": "c1"}]),
    AIMessage(content="", tool_calls=[{"name": "get_balance", "args": {"account_id": "ACC-0001"}, "id": "c2"}]),
    AIMessage(content="Your balance is 1,200.00 GBP."),
])
b = StateGraph(MessagesState)
b.add_node("agent", lambda s: {"messages": [next(replies)]})
b.add_node("tools", ToolNode([get_balance], handle_tool_errors=True))
b.add_edge(START, "agent")
b.add_conditional_edges("agent", tools_condition)
b.add_edge("tools", "agent")
out = b.compile().invoke({"messages": [HumanMessage("What's my balance?")]})
tool_msgs = [m for m in out["messages"] if m.type == "tool"]
assert tool_msgs[0].status == "error" and "expected ACC-NNNN" in tool_msgs[0].content
assert tool_msgs[1].content == "1,200.00 GBP" and out["messages"][-1].content.startswith("Your balance")
```

The error text becomes the model's observation, so write exception messages that say how to fix the call. You can also pass a custom handler or message to `handle_tool_errors` to control what the model sees. Don't leak internals (stack traces, SQL, hostnames) in these messages.

## Likely follow-ups

- What should the tool message say for a permission error?

---

[← Q0550](../../batch_06_langgraph_langchain/0550_guardrail_nodes_around_an_agent/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0552 →](../../batch_06_langgraph_langchain/0552_structured_output_node_with_validation_and_retry/README.md)

# Q0516 · A ReAct agent graph with ToolNode

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Agents | Medium |

## Question

Build a tool-calling agent loop in LangGraph (a model node, `ToolNode` and `tools_condition`) using a fake model, so the loop is deterministic in tests.

## Answer

```python
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


@tool
def get_fx_rate(pair: str) -> float:
    """Return the latest FX rate for a currency pair such as GBPUSD."""
    return {"GBPUSD": 1.27}[pair]


class ScriptedModel:
    def __init__(self, replies):
        self.replies = iter(replies)

    def __call__(self, state: MessagesState) -> dict:
        return {"messages": [next(self.replies)]}


model = ScriptedModel([
    AIMessage(content="", tool_calls=[{"name": "get_fx_rate", "args": {"pair": "GBPUSD"}, "id": "call_1"}]),
    AIMessage(content="100 GBP is about 127 USD."),
])
b = StateGraph(MessagesState)
b.add_node("agent", model)
b.add_node("tools", ToolNode([get_fx_rate]))
b.add_edge(START, "agent")
b.add_conditional_edges("agent", tools_condition)
b.add_edge("tools", "agent")
out = b.compile().invoke({"messages": [HumanMessage("Convert 100 GBP to USD")]})
assert [m.type for m in out["messages"]] == ["human", "ai", "tool", "ai"]
assert out["messages"][2].content == "1.27" and out["messages"][2].tool_call_id == "call_1"
assert out["messages"][-1].content == "100 GBP is about 127 USD."
```

`tools_condition` routes to `"tools"` when the last AI message contains tool calls, and to `END` otherwise. `ToolNode` executes the calls (in parallel when there are several) and returns `ToolMessage`s linked by `tool_call_id`. In production, the agent node calls `model.bind_tools(tools).invoke(messages)`. The scripted model replaces it for deterministic tests.

## Likely follow-ups

- How does ToolNode handle several tool calls in one AI message?

---

[← Q0515](../../batch_06_langgraph_langchain/0515_pydantic_state_validation/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0517 →](../../batch_06_langgraph_langchain/0517_custom_routing_after_the_model/README.md)

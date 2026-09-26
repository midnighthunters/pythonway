# Q0518 · create_agent in LangChain 1.x

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain agents | Medium |

## Question

Build a tool-calling agent with LangChain 1.x's `create_agent` and a fake chat model, and inspect the resulting message sequence.

## Answer

```python
from langchain.agents import create_agent
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool


class FakeToolModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


@tool
def search_policies(query: str) -> str:
    """Search internal travel and expense policies."""
    return "[pol-7] London hotels are capped at 180 GBP per night."


model = FakeToolModel(messages=iter([
    AIMessage(content="", tool_calls=[{"name": "search_policies", "args": {"query": "London hotel cap"}, "id": "c1"}]),
    AIMessage(content="The London hotel cap is 180 GBP per night [pol-7]."),
]))
agent = create_agent(model, tools=[search_policies], system_prompt="Answer from policies and cite them.")
out = agent.invoke({"messages": [HumanMessage("What's the London hotel cap?")]})
assert [type(m).__name__ for m in out["messages"]] == ["HumanMessage", "AIMessage", "ToolMessage", "AIMessage"]
assert out["messages"][-1].content.endswith("[pol-7].")
```

`create_agent` returns a compiled LangGraph graph, so it supports `stream`, checkpointers, interrupts and use as a subgraph. It replaced the older `langgraph.prebuilt.create_react_agent` as the recommended prebuilt agent. Customise it with middleware (human-in-the-loop, summarisation, dynamic prompts, model fallback) rather than rewriting the loop.

## Likely follow-ups

- What would you use middleware for, instead of a custom graph?

---

[← Q0517](../../batch_06_langgraph_langchain/0517_custom_routing_after_the_model/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0519 →](../../batch_06_langgraph_langchain/0519_agent_middleware_in_langchain_1_x/README.md)

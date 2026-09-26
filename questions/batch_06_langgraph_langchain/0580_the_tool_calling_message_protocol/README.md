# Q0580 · The tool-calling message protocol

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain tools | Medium |

## Question

Walk through LangChain's tool-calling message protocol by hand: an `AIMessage` carries tool calls, invoking the tool with a tool call returns a `ToolMessage` with the matching id, and the conversation continues.

## Answer

```python
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool


@tool
def get_balance(account_id: str) -> str:
    """Get an account balance."""
    return {"ACC-1": "1,200.00 GBP"}[account_id]


ai = AIMessage(content="", tool_calls=[
    {"name": "get_balance", "args": {"account_id": "ACC-1"}, "id": "call_abc", "type": "tool_call"}])
tool_msg = get_balance.invoke(ai.tool_calls[0])
assert isinstance(tool_msg, ToolMessage)
assert tool_msg.tool_call_id == "call_abc" and tool_msg.content == "1,200.00 GBP"
conversation = [HumanMessage("What's my balance?"), ai, tool_msg]
assert [m.type for m in conversation] == ["human", "ai", "tool"]
```

Invoking a tool with a full tool call (rather than bare arguments) returns a `ToolMessage` already linked by `tool_call_id`, which is what providers require. Every tool call in an `AIMessage` must be answered by exactly one `ToolMessage` (including errors or rejections) before the next model call, or the provider will reject the request.

## Likely follow-ups

- What must you send back when a human rejects a proposed tool call?

---

[← Q0579](../../batch_06_langgraph_langchain/0579_structuredtool_with_a_pydantic_args_schema/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0581 →](../../batch_06_langgraph_langchain/0581_message_types_and_content_blocks/README.md)

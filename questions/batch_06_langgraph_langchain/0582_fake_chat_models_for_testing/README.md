# Q0582 · Fake chat models for testing

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Testing | Easy |

## Question

Show the fake chat models in `langchain_core` for deterministic tests: fixed responses, streaming chunks and scripted tool calls.

## Answer

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel, GenericFakeChatModel
from langchain_core.messages import AIMessage

fixed = FakeListChatModel(responses=["first", "second"])
assert [fixed.invoke("a").content, fixed.invoke("b").content] == ["first", "second"]

streaming = GenericFakeChatModel(messages=iter([AIMessage(content="Hotels are capped at 180 GBP")]))
chunks = [c.content for c in streaming.stream("cap?")]
assert "".join(chunks) == "Hotels are capped at 180 GBP" and len(chunks) > 1


class FakeToolModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


tool_model = FakeToolModel(messages=iter([AIMessage(content="", tool_calls=[
    {"name": "search_policies", "args": {"query": "hotel cap"}, "id": "c1"}])]))
reply = tool_model.bind_tools([]).invoke("cap?")
assert reply.tool_calls[0]["name"] == "search_policies"
```

`FakeListChatModel` suits simple chains, `GenericFakeChatModel` streams its scripted messages token by token, and a tiny subclass with `bind_tools` scripts tool-calling agents. These make control-flow tests fast, free and deterministic, and model quality is measured separately by evaluations.

## Likely follow-ups

- What can't fake-model tests tell you?

---

[← Q0581](../../batch_06_langgraph_langchain/0581_message_types_and_content_blocks/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0583 →](../../batch_06_langgraph_langchain/0583_callbacks_for_logging_and_metrics/README.md)

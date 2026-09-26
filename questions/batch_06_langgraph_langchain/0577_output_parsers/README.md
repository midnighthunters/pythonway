# Q0577 · Output parsers

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain | Easy |

## Question

Use LangChain's `StrOutputParser` and `JsonOutputParser` on model outputs, including JSON wrapped in a markdown code fence.

## Answer

```python
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

fenced = FakeListChatModel(responses=['Here you go:\n```json\n{"label": "it", "urgent": true}\n```'])
assert (fenced | JsonOutputParser()).invoke("classify") == {"label": "it", "urgent": True}
assert (FakeListChatModel(responses=["plain text"]) | StrOutputParser()).invoke("x") == "plain text"
try:
    (FakeListChatModel(responses=["not json at all"]) | JsonOutputParser()).invoke("x")
    raise AssertionError
except OutputParserException:
    pass
```

`JsonOutputParser` strips markdown fences and parses JSON (it can also stream partial JSON). Parsers are a fallback for providers or models without native structured output. Prefer `with_structured_output(Schema)` where available, and always validate the parsed data with Pydantic before using it.

## Likely follow-ups

- What's the difference between parsing and validating model output?

---

[← Q0576](../../batch_06_langgraph_langchain/0576_chatprompttemplate_and_messagesplaceholder/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0578 →](../../batch_06_langgraph_langchain/0578_define_tools_with_the_tool_decorator/README.md)

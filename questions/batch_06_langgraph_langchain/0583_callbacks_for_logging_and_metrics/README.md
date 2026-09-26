# Q0583 · Callbacks for logging and metrics

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Observability | Medium |

## Question

Implement a LangChain callback handler that records model starts and ends and counts calls, and attach it to a chain invocation through the config.

## Answer

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class MetricsHandler(BaseCallbackHandler):
    def __init__(self) -> None:
        self.events: list[str] = []
        self.model_calls = 0

    def on_chat_model_start(self, serialized, messages, **kwargs) -> None:
        self.model_calls += 1
        self.events.append(f"model_start:{len(messages[0])} msgs")

    def on_llm_end(self, response, **kwargs) -> None:
        self.events.append(f"model_end:{response.generations[0][0].text[:12]}")


chain = ChatPromptTemplate.from_messages([("system", "Be brief."), ("human", "{q}")]) | FakeListChatModel(
    responses=["180 GBP per night"]) | StrOutputParser()
handler = MetricsHandler()
assert chain.invoke({"q": "London cap?"}, config={"callbacks": [handler], "tags": ["policy_qa"]}) == "180 GBP per night"
assert handler.model_calls == 1 and handler.events == ["model_start:2 msgs", "model_end:180 GBP per "]
```

Callbacks propagate through nested runnables and LangGraph nodes via the config. They're how tracing integrations work, and they're useful for custom metrics (latency, tokens from `usage_metadata`, error counts). Keep handlers fast and non-blocking, and never log raw prompts containing personal data from them.

## Likely follow-ups

- Why must callback handlers be fast and non-blocking?

---

[← Q0582](../../batch_06_langgraph_langchain/0582_fake_chat_models_for_testing/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0584 →](../../batch_06_langgraph_langchain/0584_read_configurable_values_inside_nodes/README.md)

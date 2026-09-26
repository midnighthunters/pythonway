# Q0574 · LCEL basics: composing runnables

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain | Easy |

## Question

Compose a prompt, a chat model and an output parser with the LangChain Expression Language (`|`), and run it with a fake model.

## Answer

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You summarise policies in one sentence for {audience}."),
    ("human", "{policy_text}"),
])
model = FakeListChatModel(responses=["Hotels in London are capped at 180 GBP per night."])
chain = prompt | model | StrOutputParser()

out = chain.invoke({"audience": "new joiners", "policy_text": "Section 4.2: hotel caps..."})
assert out == "Hotels in London are capped at 180 GBP per night."
rendered = prompt.invoke({"audience": "new joiners", "policy_text": "x"}).to_messages()
assert rendered[0].content == "You summarise policies in one sentence for new joiners."
assert chain.batch([{"audience": "a", "policy_text": "p"}]) and hasattr(chain, "stream")
```

Every component is a `Runnable` with `invoke`, `batch`, `stream` and async variants, so chains get batching, streaming and tracing for free. LCEL suits linear pipelines. Once you need loops, branching with state, persistence or human-in-the-loop, move to LangGraph and use chains inside nodes.

## Likely follow-ups

- When does an LCEL chain become the wrong abstraction?

---

[← Q0573](../../batch_06_langgraph_langchain/0573_model_fallbacks_with_with_fallbacks/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0575 →](../../batch_06_langgraph_langchain/0575_runnableparallel_and_runnablepassthrough/README.md)

# Q0575 · RunnableParallel and RunnablePassthrough

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain | Medium |

## Question

Build a small RAG chain in which a retriever and the original question run in parallel into the prompt, using `RunnableParallel` and `RunnablePassthrough`, and capture the rendered prompt for inspection.

## Answer

```python
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

DOCS = {"hotel": "[1] London hotels capped at 180 GBP.", "claims": "[2] File claims within 30 days."}
retriever = RunnableLambda(lambda q: "\n".join(v for k, v in DOCS.items() if k in q.lower()))
captured = {}


def capture(prompt_value):
    captured["messages"] = prompt_value.to_messages()
    return prompt_value


prompt = ChatPromptTemplate.from_messages([("system", "Answer only from:\n{context}"), ("human", "{question}")])
chain = (RunnableParallel(context=retriever, question=RunnablePassthrough())
         | prompt | RunnableLambda(capture) | FakeListChatModel(responses=["180 GBP [1]"]) | StrOutputParser())
assert chain.invoke("What is the hotel cap?") == "180 GBP [1]"
assert captured["messages"][0].content == "Answer only from:\n[1] London hotels capped at 180 GBP."
assert captured["messages"][1].content == "What is the hotel cap?"
```

`RunnableParallel` runs its branches concurrently with the same input, and `RunnablePassthrough` forwards the input unchanged. Inserting a capturing `RunnableLambda` is a handy debugging and test technique for seeing exactly what reaches the model.

## Likely follow-ups

- How would you add the retrieved document ids to the chain's output as well as the answer?

---

[← Q0574](../../batch_06_langgraph_langchain/0574_lcel_basics_composing_runnables/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0576 →](../../batch_06_langgraph_langchain/0576_chatprompttemplate_and_messagesplaceholder/README.md)

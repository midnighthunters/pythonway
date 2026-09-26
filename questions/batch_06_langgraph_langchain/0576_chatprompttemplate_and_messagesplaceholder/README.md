# Q0576 · ChatPromptTemplate and MessagesPlaceholder

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain | Medium |

## Question

Build a chat prompt with a system message, a placeholder for the conversation history, and the new user question. Show the rendered message order, and how to include literal braces.

## Answer

```python
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", 'You are the policy assistant. Reply as JSON like {{"answer": "...", "sources": [1]}}.'),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
msgs = prompt.format_messages(history=[HumanMessage("London cap?"), AIMessage("180 GBP [1]")],
                              question="And Paris?")
assert [m.type for m in msgs] == ["system", "human", "ai", "human"]
assert msgs[0].content.endswith('Reply as JSON like {"answer": "...", "sources": [1]}.')
assert msgs[-1].content == "And Paris?"
assert set(prompt.input_variables) == {"history", "question"}
```

Doubling the braces (`{{ }}`) inserts literal JSON braces, because single braces are template variables. `MessagesPlaceholder` injects real message objects (preserving roles and tool calls), which is much better than pasting history as text. The prompt's `input_variables` also makes a good contract check in tests.

## Likely follow-ups

- Why is injecting history as message objects better than a single text block?

---

[← Q0575](../../batch_06_langgraph_langchain/0575_runnableparallel_and_runnablepassthrough/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0577 →](../../batch_06_langgraph_langchain/0577_output_parsers/README.md)

# Q0532 · Stream LLM tokens with messages mode

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Streaming | Medium |

## Question

Stream tokens from a model call inside a LangGraph node using `stream_mode="messages"`, and show how to tell which node produced them.

## Answer

```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph

model = GenericFakeChatModel(messages=iter([AIMessage(content="The cap is 180 GBP")]))


def answer(state: MessagesState) -> dict:
    return {"messages": [model.invoke(state["messages"])]}


b = StateGraph(MessagesState)
b.add_node("answer", answer)
b.add_edge(START, "answer")
b.add_edge("answer", END)

tokens, nodes = [], set()
for chunk, meta in b.compile().stream({"messages": [HumanMessage("London cap?")]}, stream_mode="messages"):
    tokens.append(chunk.content)
    nodes.add(meta["langgraph_node"])
assert "".join(tokens) == "The cap is 180 GBP" and len(tokens) > 1 and nodes == {"answer"}
```

The node calls `model.invoke` normally. LangGraph's callback integration captures the model's token stream even though the node itself doesn't stream. The metadata identifies the node (and more), so you can stream only the final answer node's tokens to the user and hide intermediate planner or tool-selection tokens.

## Likely follow-ups

- Why might you hide tokens from a planning node?

---

[← Q0531](../../batch_06_langgraph_langchain/0531_stream_node_updates_to_a_client/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0533 →](../../batch_06_langgraph_langchain/0533_custom_progress_events_with_get_stream_writer/README.md)

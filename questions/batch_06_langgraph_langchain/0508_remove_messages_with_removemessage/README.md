# Q0508 · Remove messages with RemoveMessage

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Messages | Medium |

## Question

Long agent conversations need pruning. Write a node that deletes all but the last N messages from the state using `RemoveMessage`.

## Answer

```python
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langgraph.graph import END, START, MessagesState, StateGraph

KEEP = 2


def prune(state: MessagesState) -> dict:
    return {"messages": [RemoveMessage(id=m.id) for m in state["messages"][:-KEEP]]}


b = StateGraph(MessagesState)
b.add_node("prune", prune)
b.add_edge(START, "prune")
b.add_edge("prune", END)
history = [HumanMessage("q1", id="1"), AIMessage("a1", id="2"), HumanMessage("q2", id="3"), AIMessage("a2", id="4")]
out = b.compile().invoke({"messages": history})
assert [m.content for m in out["messages"]] == ["q2", "a2"]
```

`RemoveMessage(id=...)` tells `add_messages` to delete that message from the persisted state, which also shrinks future checkpoints. Pitfalls: never leave an assistant tool-call message without its tool results (or the other way round), because providers reject orphaned tool messages. Prune in whole turns, and consider summarising before deleting.

## Likely follow-ups

- Why is deleting from the state different from trimming only what you send to the model?

---

[← Q0507](../../batch_06_langgraph_langchain/0507_messagesstate_and_add_messages_semantics/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0509 →](../../batch_06_langgraph_langchain/0509_conditional_edges_for_routing/README.md)

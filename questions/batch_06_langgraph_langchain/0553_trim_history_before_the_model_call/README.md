# Q0553 · Trim history before the model call

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Context management | Medium |

## Question

Keep the full conversation in the checkpointed state, but send the model only the most recent messages that fit a token budget, using `trim_messages`.

## Answer

```python
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages
from langgraph.graph import END, START, MessagesState, StateGraph

seen_by_model: list[list[str]] = []


def count_words(messages) -> int:
    return sum(len(m.content.split()) for m in messages)


def agent(state: MessagesState) -> dict:
    window = trim_messages(state["messages"], max_tokens=12, token_counter=count_words, strategy="last",
                           include_system=True, start_on="human")
    seen_by_model.append([m.content for m in window])
    return {"messages": [AIMessage("ok")]}


b = StateGraph(MessagesState)
b.add_node("agent", agent)
b.add_edge(START, "agent")
b.add_edge("agent", END)
history = [SystemMessage("Be concise."), HumanMessage("first question about hotel caps please"),
           AIMessage("London is 180 GBP"), HumanMessage("and Paris?"), AIMessage("160 EUR"), HumanMessage("thanks, and Rome?")]
out = b.compile().invoke({"messages": history})
assert len(out["messages"]) == 7
assert seen_by_model[0][0] == "Be concise." and seen_by_model[0][-1] == "thanks, and Rome?"
assert "first question about hotel caps please" not in seen_by_model[0]
```

Trimming the input keeps the state complete (for audit and later summarisation), while the model sees a bounded window. `include_system=True` keeps the system prompt, and `start_on="human"` avoids starting the window with an orphaned AI or tool message. Use the model's real token counter in production.

## Likely follow-ups

- When would you delete messages from the state instead of trimming the input?

---

[← Q0552](../../batch_06_langgraph_langchain/0552_structured_output_node_with_validation_and_retry/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0554 →](../../batch_06_langgraph_langchain/0554_summarise_long_conversations_in_a_graph/README.md)

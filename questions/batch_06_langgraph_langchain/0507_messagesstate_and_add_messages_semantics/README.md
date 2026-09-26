# Q0507 · MessagesState and add_messages semantics

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Messages | Medium |

## Question

Explain how the `add_messages` reducer merges message lists (appending new messages and replacing messages with the same id), and demonstrate it directly.

## Answer

```python
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages

existing = [HumanMessage("What's the London cap?", id="1"), AIMessage("Checking...", id="2")]
update = [AIMessage("The cap is 180 GBP [1].", id="2"), HumanMessage("And Paris?", id="3")]
merged = add_messages(existing, update)
assert [m.content for m in merged] == ["What's the London cap?", "The cap is 180 GBP [1].", "And Paris?"]
assert [m.id for m in merged] == ["1", "2", "3"]

no_ids = add_messages([], [HumanMessage("hi")])
assert no_ids[0].id is not None
```

Rules:
- Messages whose id isn't in the existing list are appended.
- A message whose id matches an existing one replaces it in place. This is how you edit or finalise a message (for example replacing a streaming placeholder).
- Messages without ids are assigned one.
- Dicts or tuples such as `("user", "hi")` are coerced into message objects.

`MessagesState` is a ready-made state with `messages: Annotated[list, add_messages]`. Extend it with your own keys for real agents.

## Likely follow-ups

- How would you edit a tool result that turned out to be wrong?

---

[← Q0506](../../batch_06_langgraph_langchain/0506_custom_reducer_for_merging_dictionaries/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0508 →](../../batch_06_langgraph_langchain/0508_remove_messages_with_removemessage/README.md)

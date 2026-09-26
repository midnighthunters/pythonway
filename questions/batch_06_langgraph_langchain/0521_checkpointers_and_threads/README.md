# Q0521 · Checkpointers and threads

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Persistence | Medium |

## Question

Show how a checkpointer and `thread_id` give each conversation its own persistent state across invocations, and how two threads stay isolated.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    notes: Annotated[list[str], operator.add]


b = StateGraph(State)
b.add_node("record", lambda s: {})
b.add_edge(START, "record")
b.add_edge("record", END)
app = b.compile(checkpointer=InMemorySaver())

priya = {"configurable": {"thread_id": "user-priya:conv-1"}}
tom = {"configurable": {"thread_id": "user-tom:conv-1"}}
app.invoke({"notes": ["prefers aisle"]}, priya)
app.invoke({"notes": ["home office Canary Wharf"]}, priya)
app.invoke({"notes": ["vegetarian"]}, tom)
assert app.get_state(priya).values["notes"] == ["prefers aisle", "home office Canary Wharf"]
assert app.get_state(tom).values["notes"] == ["vegetarian"]
```

Each invocation on the same thread continues from its latest checkpoint, and new input is merged through the reducers. Threads are the isolation unit, so derive thread ids server-side, make them unguessable, bind them to the owning user, and check ownership on every access. Never accept a raw thread id from a client without that check. `InMemorySaver` is for tests. Production uses a durable checkpointer.

## Likely follow-ups

- What goes wrong if thread ids are sequential integers taken from the client?

---

[← Q0520](../../batch_06_langgraph_langchain/0520_human_in_the_loop_middleware/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0522 →](../../batch_06_langgraph_langchain/0522_choosing_a_production_checkpointer/README.md)

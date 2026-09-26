# Q0558 · Compile-time validation errors

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Easy |

## Question

What mistakes does `StateGraph.compile()` (and graph building) catch early? Demonstrate two.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    x: int


b = StateGraph(State)
b.add_node("a", lambda s: {"x": 1})
b.add_edge(START, "missing_node")
try:
    b.compile()
    raise AssertionError("expected compile error")
except ValueError as e:
    assert "unknown node" in str(e)

dup = StateGraph(State)
dup.add_node("a", lambda s: {"x": 1})
try:
    dup.add_node("a", lambda s: {"x": 2})
    raise AssertionError("expected duplicate error")
except ValueError:
    pass

ok = StateGraph(State)
ok.add_node("a", lambda s: {"x": s["x"] + 1})
ok.add_edge(START, "a")
ok.add_edge("a", END)
assert ok.compile().invoke({"x": 1}) == {"x": 2}
```

Structural checks (unknown nodes, duplicates, missing entry points) happen at build or compile time. Behavioural problems (a conditional function returning an undeclared node, runaway loops, state conflicts from parallel writes) only show up at runtime, which is why trajectory tests and recursion limits matter.

## Likely follow-ups

- Which graph bugs can only be found at runtime?

---

[← Q0557](../../batch_06_langgraph_langchain/0557_assert_trajectories_from_streamed_updates/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0559 →](../../batch_06_langgraph_langchain/0559_typeddict_dataclass_or_pydantic_state/README.md)

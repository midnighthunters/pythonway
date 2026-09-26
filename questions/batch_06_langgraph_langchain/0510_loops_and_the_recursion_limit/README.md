# Q0510 · Loops and the recursion limit

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Build a loop (a node that retries until a condition holds) and show how LangGraph's recursion limit stops a runaway loop.

## Answer

```python
from typing import TypedDict

from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    attempts: int
    ok: bool


def try_step(state: State) -> dict:
    n = state["attempts"] + 1
    return {"attempts": n, "ok": n >= 3}


def again(state: State) -> str:
    return END if state["ok"] else "try_step"


b = StateGraph(State)
b.add_node("try_step", try_step)
b.add_edge(START, "try_step")
b.add_conditional_edges("try_step", again, ["try_step", END])
g = b.compile()
assert g.invoke({"attempts": 0, "ok": False}) == {"attempts": 3, "ok": True}

never = StateGraph(State)
never.add_node("spin", lambda s: {"attempts": s["attempts"] + 1})
never.add_edge(START, "spin")
never.add_edge("spin", "spin")
try:
    never.compile().invoke({"attempts": 0, "ok": False}, {"recursion_limit": 5})
    raise AssertionError("should have stopped")
except GraphRecursionError:
    pass
```

The recursion limit caps the number of supersteps per run (there is a default, and you can set `recursion_limit` in the config). It is a safety net, not a design tool: add explicit loop conditions and budgets in the state (attempt counters, `RemainingSteps`), so the graph can finish gracefully instead of raising.

## Likely follow-ups

- How would you return a graceful message just before hitting the limit?

---

[← Q0509](../../batch_06_langgraph_langchain/0509_conditional_edges_for_routing/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0511 →](../../batch_06_langgraph_langchain/0511_update_and_route_with_command/README.md)

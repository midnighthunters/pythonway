# Q0556 · Unit-test nodes and graphs

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Testing | Medium |

## Question

Show how to test LangGraph code at two levels: pure node functions with plain dict states, and the compiled graph's routing with fake nodes.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    amount: float
    route: str
    result: str


def triage(state: State) -> dict:
    return {"route": "auto" if state["amount"] <= 100 else "review"}


def build(auto_node, review_node):
    b = StateGraph(State)
    b.add_node("triage", triage)
    b.add_node("auto", auto_node)
    b.add_node("review", review_node)
    b.add_edge(START, "triage")
    b.add_conditional_edges("triage", lambda s: s["route"], ["auto", "review"])
    b.add_edge("auto", END)
    b.add_edge("review", END)
    return b.compile()


# 1) node-level tests: plain functions, no graph needed
assert triage({"amount": 50.0, "route": "", "result": ""}) == {"route": "auto"}
assert triage({"amount": 100.01, "route": "", "result": ""}) == {"route": "review"}

# 2) graph-level tests: swap real side-effecting nodes for fakes and assert routing
calls: list[str] = []
g = build(lambda s: calls.append("auto") or {"result": "paid"}, lambda s: calls.append("review") or {"result": "queued"})
assert g.invoke({"amount": 900.0, "route": "", "result": ""})["result"] == "queued" and calls == ["review"]
```

Build graphs from a factory that accepts node implementations (dependency injection), so tests can substitute fakes for model calls and side effects. Test boundaries (exactly 100), and test the graph wiring separately from node logic.

## Likely follow-ups

- What would you inject to test a node that calls an LLM?

---

[← Q0555](../../batch_06_langgraph_langchain/0555_visualise_a_graph_as_mermaid/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0557 →](../../batch_06_langgraph_langchain/0557_assert_trajectories_from_streamed_updates/README.md)

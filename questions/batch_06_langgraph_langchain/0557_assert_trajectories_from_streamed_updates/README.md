# Q0557 · Assert trajectories from streamed updates

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Testing | Medium |

## Question

Write a test helper that runs a graph with `stream_mode="updates"` and returns the ordered list of nodes that executed, then assert expected trajectories for different inputs.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    amount: float
    status: str


def trajectory(graph, inputs: dict) -> list[str]:
    return [node for chunk in graph.stream(inputs, stream_mode="updates") for node in chunk]


b = StateGraph(State)
b.add_node("validate", lambda s: {"status": "valid" if s["amount"] > 0 else "invalid"})
b.add_node("risk_check", lambda s: {"status": "checked"})
b.add_node("pay", lambda s: {"status": "paid"})
b.add_node("reject", lambda s: {"status": "rejected"})
b.add_edge(START, "validate")
b.add_conditional_edges("validate", lambda s: "risk_check" if s["status"] == "valid" else "reject", ["risk_check", "reject"])
b.add_conditional_edges("risk_check", lambda s: "pay" if s["amount"] < 10_000 else "reject", ["pay", "reject"])
b.add_edge("pay", END)
b.add_edge("reject", END)
g = b.compile()
assert trajectory(g, {"amount": 500.0, "status": ""}) == ["validate", "risk_check", "pay"]
assert trajectory(g, {"amount": -5.0, "status": ""}) == ["validate", "reject"]
assert trajectory(g, {"amount": 50_000.0, "status": ""}) == ["validate", "risk_check", "reject"]
```

Trajectory assertions catch wiring regressions, such as a refactor that lets payments skip the risk check. That is precisely the kind of control auditors care about. Keep a table of input-to-trajectory cases for critical paths.

## Likely follow-ups

- How would you test that `pay` can never run without `risk_check` for any input?

---

[← Q0556](../../batch_06_langgraph_langchain/0556_unit_test_nodes_and_graphs/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0558 →](../../batch_06_langgraph_langchain/0558_compile_time_validation_errors/README.md)

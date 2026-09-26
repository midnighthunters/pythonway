# Q0545 · Remaining steps for graceful stops

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Reliability | Medium |

## Question

Use the managed `RemainingSteps` value so an agent loop wraps up with a partial answer just before hitting the recursion limit, instead of raising an error.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.managed import RemainingSteps


class State(TypedDict):
    findings: list[str]
    answer: str
    remaining_steps: RemainingSteps


def research(state: State) -> dict:
    if state["remaining_steps"] <= 2:
        return {"answer": f"Partial answer from {len(state['findings'])} findings; more research needed."}
    return {"findings": state["findings"] + [f"finding {len(state['findings']) + 1}"]}


def keep_going(state: State) -> str:
    return END if state["answer"] else "research"


b = StateGraph(State)
b.add_node("research", research)
b.add_edge(START, "research")
b.add_conditional_edges("research", keep_going, ["research", END])
out = b.compile().invoke({"findings": [], "answer": ""}, {"recursion_limit": 6})
assert out["answer"].startswith("Partial answer from") and len(out["findings"]) >= 1
```

`RemainingSteps` is filled in by the runtime from the recursion limit, so nodes can see how much budget is left. Returning an honest partial answer with a clear status is far better for users than an exception. Pair it with token and cost budgets.

## Likely follow-ups

- What should the partial answer tell the user?

---

[← Q0544](../../batch_06_langgraph_langchain/0544_functional_api_versus_graph_api/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0546 →](../../batch_06_langgraph_langchain/0546_supervisor_pattern_in_langgraph/README.md)

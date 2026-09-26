# Q0548 · Plan-and-execute in LangGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Planning | Medium |

## Question

Implement plan-and-execute as a LangGraph graph: a planner node writes a plan, an executor node runs one step per loop iteration, and a finaliser runs when the plan is exhausted.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

TOOLS = {"lookup_employee": lambda arg: "E-17", "leave_balance": lambda arg: 12}


class State(TypedDict):
    goal: str
    plan: list[dict]
    results: Annotated[list, operator.add]
    answer: str


def planner(state: State) -> dict:
    return {"plan": [{"tool": "lookup_employee", "arg": "Priya"}, {"tool": "leave_balance", "arg": "$prev"}]}


def executor(state: State) -> dict:
    step, rest = state["plan"][0], state["plan"][1:]
    arg = state["results"][-1] if step["arg"] == "$prev" else step["arg"]
    return {"plan": rest, "results": [TOOLS[step["tool"]](arg)]}


def finalize(state: State) -> dict:
    return {"answer": f"Priya has {state['results'][-1]} leave days."}


b = StateGraph(State)
b.add_node("planner", planner)
b.add_node("executor", executor)
b.add_node("finalize", finalize)
b.add_edge(START, "planner")
b.add_edge("planner", "executor")
b.add_conditional_edges("executor", lambda s: "executor" if s["plan"] else "finalize", ["executor", "finalize"])
b.add_edge("finalize", END)
out = b.compile().invoke({"goal": "leave days for Priya", "plan": [], "results": [], "answer": ""})
assert out["results"] == ["E-17", 12] and out["answer"] == "Priya has 12 leave days."
```

Because each step is its own superstep, you get a checkpoint after every tool call (resumable), per-step streaming updates, and a natural place for an approval interrupt before side-effecting steps. Add a re-planner node on the failure path.

## Likely follow-ups

- Where would you add the approval interrupt?

---

[← Q0547](../../batch_06_langgraph_langchain/0547_handoffs_between_agents_with_command/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0549 →](../../batch_06_langgraph_langchain/0549_reflection_loop_in_langgraph/README.md)

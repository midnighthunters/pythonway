# Q0549 · Reflection loop in LangGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Self-refinement | Medium |

## Question

Build a generate → critique loop in LangGraph with a round counter, so the draft is revised until the critic finds no issues or three rounds pass.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    draft: str
    issues: list[str]
    rounds: int


def generate(state: State) -> dict:
    draft = state["draft"] or "The London cap is 180 GBP"
    if "missing citation" in state["issues"]:
        draft += " [pol-7]"
    if "no period" in state["issues"]:
        draft += "."
    return {"draft": draft, "rounds": state["rounds"] + 1}


def critique(state: State) -> dict:
    issues = []
    if "[pol-" not in state["draft"]:
        issues.append("missing citation")
    if not state["draft"].endswith("."):
        issues.append("no period")
    return {"issues": issues}


def should_continue(state: State) -> str:
    return "generate" if state["issues"] and state["rounds"] < 3 else END


b = StateGraph(State)
b.add_node("generate", generate)
b.add_node("critique", critique)
b.add_edge(START, "generate")
b.add_edge("generate", "critique")
b.add_conditional_edges("critique", should_continue, ["generate", END])
out = b.compile().invoke({"draft": "", "issues": [], "rounds": 0})
assert out == {"draft": "The London cap is 180 GBP [pol-7].", "issues": [], "rounds": 2}
```

Deterministic critics (format, citation and validator checks) are cheap and reliable. LLM critics need specific rubrics. The round counter in the state gives a hard cap independent of the recursion limit.

## Likely follow-ups

- How would you record each round's critique for evaluation?

---

[← Q0548](../../batch_06_langgraph_langchain/0548_plan_and_execute_in_langgraph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0550 →](../../batch_06_langgraph_langchain/0550_guardrail_nodes_around_an_agent/README.md)

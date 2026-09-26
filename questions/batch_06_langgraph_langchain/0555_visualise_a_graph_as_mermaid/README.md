# Q0555 · Visualise a graph as Mermaid

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Tooling | Easy |

## Question

Render a compiled graph's structure as a Mermaid diagram for design reviews and documentation.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    route: str


b = StateGraph(State)
b.add_node("classify", lambda s: {"route": "policy"})
b.add_node("policy_qa", lambda s: {})
b.add_node("escalate", lambda s: {})
b.add_edge(START, "classify")
b.add_conditional_edges("classify", lambda s: "policy_qa" if s["route"] == "policy" else "escalate",
                        ["policy_qa", "escalate"])
b.add_edge("policy_qa", END)
b.add_edge("escalate", END)
mermaid = b.compile().get_graph().draw_mermaid()
assert "graph TD" in mermaid
assert all(name in mermaid for name in ("classify", "policy_qa", "escalate"))
```

Declaring the conditional destinations (the list argument, or `Command[Literal[...]]` annotations) is what lets the diagram show every possible path. Commit the Mermaid output next to the code, or generate it in CI, so reviewers (including risk and compliance) can see the control flow without reading Python.

## Likely follow-ups

- Why is an accurate graph diagram useful for model-risk reviews?

---

[← Q0554](../../batch_06_langgraph_langchain/0554_summarise_long_conversations_in_a_graph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0556 →](../../batch_06_langgraph_langchain/0556_unit_test_nodes_and_graphs/README.md)

# Q0534 · Subgraphs as nodes

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Composition | Medium |

## Question

Compose a compiled subgraph as a node in a parent graph (for example a reusable "retrieve and answer" subgraph inside an assistant workflow), sharing state keys.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    answer: str
    trace: Annotated[list[str], operator.add]


rag = StateGraph(State)
rag.add_node("retrieve", lambda s: {"trace": ["rag.retrieve"]})
rag.add_node("generate", lambda s: {"answer": f"Answer to: {s['question']}", "trace": ["rag.generate"]})
rag.add_edge(START, "retrieve")
rag.add_edge("retrieve", "generate")
rag.add_edge("generate", END)
rag_graph = rag.compile()

def build_parent(rag_node) -> StateGraph:
    p = StateGraph(State)
    p.add_node("guard_input", lambda s: {"trace": ["guard_input"]})
    p.add_node("rag", rag_node)
    p.add_node("guard_output", lambda s: {"trace": ["guard_output"]})
    p.add_edge(START, "guard_input")
    p.add_edge("guard_input", "rag")
    p.add_edge("rag", "guard_output")
    p.add_edge("guard_output", END)
    return p


inp = {"question": "London cap?", "answer": "", "trace": []}
direct = build_parent(rag_graph).compile().invoke(inp)
assert direct["trace"] == ["guard_input", "guard_input", "rag.retrieve", "rag.generate", "guard_output"]


def call_rag(state: State) -> dict:
    out = rag_graph.invoke({"question": state["question"], "answer": "", "trace": []})
    return {"answer": out["answer"], "trace": out["trace"]}


wrapped = build_parent(call_rag).compile().invoke(inp)
assert wrapped["answer"] == "Answer to: London cap?"
assert wrapped["trace"] == ["guard_input", "rag.retrieve", "rag.generate", "guard_output"]
```

Adding a compiled subgraph directly as a node works when the parent and subgraph share state keys. Note the gotcha: the subgraph returns its whole final state, including the `trace` entries it received from the parent, so the parent's `operator.add` reducer appends them a second time ("guard_input" appears twice). Two fixes:
- Call the subgraph inside a wrapper node and return only the new information (as above).
- Give the subgraph its own schema, so reducer keys don't overlap.

Subgraphs give teams reusable, separately testable components (a RAG subgraph, a compliance-check subgraph), and they're how multi-agent systems nest agents. Use `subgraphs=True` when streaming to see inner events. The parent's checkpointer propagates to a subgraph added as a node.

## Likely follow-ups

- How do you compose a subgraph whose state schema is different from the parent's?

---

[← Q0533](../../batch_06_langgraph_langchain/0533_custom_progress_events_with_get_stream_writer/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0535 →](../../batch_06_langgraph_langchain/0535_subgraph_with_its_own_state_schema/README.md)

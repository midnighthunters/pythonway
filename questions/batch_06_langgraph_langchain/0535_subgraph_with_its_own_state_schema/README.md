# Q0535 · Subgraph with its own state schema

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Composition | Medium |

## Question

A RAG subgraph uses its own state (`query`, `chunks`, `draft`) while the parent uses `question`, `answer` and `trace`. Connect them with an adapter node that maps the inputs and outputs explicitly.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class RagState(TypedDict):
    query: str
    chunks: list[str]
    draft: str


rag = StateGraph(RagState)
rag.add_node("retrieve", lambda s: {"chunks": ["[1] London cap 180 GBP", "[2] Paris cap 160 EUR"]})
rag.add_node("write", lambda s: {"draft": f"{s['query']} -> 180 GBP {s['chunks'][0][:3]}"})
rag.add_edge(START, "retrieve")
rag.add_edge("retrieve", "write")
rag.add_edge("write", END)
rag_graph = rag.compile()


class Parent(TypedDict):
    question: str
    answer: str
    trace: Annotated[list[str], operator.add]


def rag_adapter(state: Parent) -> dict:
    out = rag_graph.invoke({"query": state["question"], "chunks": [], "draft": ""})
    return {"answer": out["draft"], "trace": [f"rag used {len(out['chunks'])} chunks"]}


p = StateGraph(Parent)
p.add_node("rag", rag_adapter)
p.add_edge(START, "rag")
p.add_edge("rag", END)
res = p.compile().invoke({"question": "London cap?", "answer": "", "trace": []})
assert res == {"question": "London cap?", "answer": "London cap? -> 180 GBP [1]", "trace": ["rag used 2 chunks"]}
```

The adapter is an explicit contract between teams: the parent never sees the subgraph's internal fields (chunks stay private), and either side can change its internals freely. This is the same data-minimisation idea as input and output schemas, applied between components.

## Likely follow-ups

- What do you lose by invoking the subgraph inside a function instead of adding it as a node?

---

[← Q0534](../../batch_06_langgraph_langchain/0534_subgraphs_as_nodes/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0536 →](../../batch_06_langgraph_langchain/0536_runtime_context_with_context_schema/README.md)

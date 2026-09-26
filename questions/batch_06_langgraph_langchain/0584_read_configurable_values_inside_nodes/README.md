# Q0584 · Read configurable values inside nodes

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Configuration | Medium |

## Question

Pass per-invocation settings (a model tier, a feature flag, a multiplier) through `config["configurable"]`, read them inside a node, and run the same compiled graph with different configurations.

## Answer

```python
from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    answer: str


def answer(state: State, config: RunnableConfig) -> dict:
    cfg = config.get("configurable", {})
    tier = cfg.get("model_tier", "small")
    style = "with citations" if cfg.get("require_citations", True) else "without citations"
    return {"answer": f"[{tier}] answer {style}"}


b = StateGraph(State)
b.add_node("answer", answer)
b.add_edge(START, "answer")
b.add_edge("answer", END)
g = b.compile()
assert g.invoke({"question": "q", "answer": ""})["answer"] == "[small] answer with citations"
assert g.invoke({"question": "q", "answer": ""},
                {"configurable": {"model_tier": "large", "require_citations": False}})["answer"] == (
    "[large] answer without citations")
```

This is how one graph backs several assistants (different models, prompts or features per tenant or experiment). The configuration is set by the server, not the end user. `thread_id` also lives in `configurable`. For typed, run-scoped dependencies (the user or tenant), the runtime `context_schema` is the newer, more explicit option.

## Likely follow-ups

- Which values belong in `configurable` and which in the runtime context?

---

[← Q0583](../../batch_06_langgraph_langchain/0583_callbacks_for_logging_and_metrics/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0585 →](../../batch_06_langgraph_langchain/0585_provider_agnostic_model_initialisation/README.md)

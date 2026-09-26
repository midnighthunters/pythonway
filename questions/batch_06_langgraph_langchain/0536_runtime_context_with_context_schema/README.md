# Q0536 · Runtime context with context_schema

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Configuration | Medium |

## Question

Pass per-run, non-state context (user id, tenant, locale) to nodes through LangGraph's runtime context, instead of stuffing it into the state or into globals.

## Answer

```python
from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime


@dataclass(frozen=True)
class RequestContext:
    user_id: str
    tenant: str
    locale: str = "en-GB"


class State(TypedDict):
    question: str
    answer: str


def answer(state: State, runtime: Runtime[RequestContext]) -> dict:
    ctx = runtime.context
    return {"answer": f"[{ctx.tenant}/{ctx.locale}] answer for {ctx.user_id}: {state['question']}"}


b = StateGraph(State, context_schema=RequestContext)
b.add_node("answer", answer)
b.add_edge(START, "answer")
b.add_edge("answer", END)
g = b.compile()
out = g.invoke({"question": "cap?", "answer": ""}, context=RequestContext(user_id="u-priya", tenant="treasury"))
assert out["answer"] == "[treasury/en-GB] answer for u-priya: cap?"
```

Context is set by the server from the authenticated request. It isn't checkpointed as state, and the model can't change it. Use it for identity, tenant, feature flags and model choice. Keep secrets out of it where possible: pass handles or clients that fetch credentials, rather than raw tokens.

## Likely follow-ups

- Why is context safer than putting `user_id` in the state?

---

[← Q0535](../../batch_06_langgraph_langchain/0535_subgraph_with_its_own_state_schema/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0537 →](../../batch_06_langgraph_langchain/0537_long_term_memory_with_the_store/README.md)

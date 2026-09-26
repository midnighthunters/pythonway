# Q0540 · Retry policies on nodes

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Reliability | Medium |

## Question

Attach a retry policy to a node that calls a flaky downstream API, so transient errors are retried with backoff and other errors fail immediately.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy

attempts = {"fx": 0, "bad": 0}


class State(TypedDict):
    rate: float


def fetch_fx(state: State) -> dict:
    attempts["fx"] += 1
    if attempts["fx"] < 3:
        raise ConnectionError("503 from FX service")
    return {"rate": 1.27}


def validate(state: State) -> dict:
    attempts["bad"] += 1
    raise ValueError("rate out of range")


policy = RetryPolicy(max_attempts=3, initial_interval=0.01, jitter=False, retry_on=ConnectionError)
b = StateGraph(State)
b.add_node("fetch_fx", fetch_fx, retry_policy=policy)
b.add_edge(START, "fetch_fx")
b.add_edge("fetch_fx", END)
assert b.compile().invoke({"rate": 0.0}) == {"rate": 1.27} and attempts["fx"] == 3

b2 = StateGraph(State)
b2.add_node("validate", validate, retry_policy=policy)
b2.add_edge(START, "validate")
b2.add_edge("validate", END)
try:
    b2.compile().invoke({"rate": 0.0})
    raise AssertionError
except ValueError:
    assert attempts["bad"] == 1
```

`retry_on` restricts retries to transient failures, so a validation bug isn't retried pointlessly. Only retry idempotent nodes, or protect side effects with idempotency keys. Retries re-run the whole node, and they happen within the same superstep.

## Likely follow-ups

- What's the danger of retrying a node that sends a payment?

---

[← Q0539](../../batch_06_langgraph_langchain/0539_use_the_store_inside_nodes/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0541 →](../../batch_06_langgraph_langchain/0541_cache_expensive_nodes_with_cachepolicy/README.md)

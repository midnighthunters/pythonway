# Q0571 · Timeouts inside nodes

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Reliability | Medium |

## Question

A node calls a slow external service. Enforce a timeout inside the async node, and degrade gracefully (return a partial result and a flag) instead of failing the whole run.

## Answer

```python
import asyncio
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    fx_rate: float | None
    degraded: bool


async def slow_fx_service() -> float:
    await asyncio.sleep(1.0)
    return 1.27


async def get_fx(state: State) -> dict:
    try:
        return {"fx_rate": await asyncio.wait_for(slow_fx_service(), timeout=0.05), "degraded": False}
    except asyncio.TimeoutError:
        return {"fx_rate": None, "degraded": True}


async def answer(state: State) -> dict:
    return {}


b = StateGraph(State)
b.add_node("get_fx", get_fx)
b.add_node("answer", answer)
b.add_edge(START, "get_fx")
b.add_edge("get_fx", "answer")
b.add_edge("answer", END)
out = asyncio.run(b.compile().ainvoke({"fx_rate": None, "degraded": False}))
assert out == {"fx_rate": None, "degraded": True}
```

Downstream nodes read the `degraded` flag and tell the user ("I couldn't get a live FX rate; here's the rest of the answer"). Pick per-call timeouts from the request's remaining deadline, and combine them with retry policies for transient errors, with the total bounded by the deadline.

## Likely follow-ups

- How do timeouts and retry policies interact?

---

[← Q0570](../../batch_06_langgraph_langchain/0570_limit_parallelism_with_max_concurrency/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0572 →](../../batch_06_langgraph_langchain/0572_error_handling_strategy_in_langgraph/README.md)

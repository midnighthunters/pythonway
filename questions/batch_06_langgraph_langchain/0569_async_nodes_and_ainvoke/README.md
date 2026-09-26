# Q0569 · Async nodes and ainvoke

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Concurrency | Medium |

## Question

Write async nodes that call I/O-bound services, run two of them in parallel branches with `ainvoke`, and show the total time is close to the slower branch rather than the sum.

## Answer

```python
import asyncio
import operator
import time
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    results: Annotated[list[str], operator.add]


async def search_flights(state: State) -> dict:
    await asyncio.sleep(0.2)
    return {"results": ["flights"]}


async def search_hotels(state: State) -> dict:
    await asyncio.sleep(0.2)
    return {"results": ["hotels"]}


b = StateGraph(State)
b.add_node("flights", search_flights)
b.add_node("hotels", search_hotels)
b.add_edge(START, "flights")
b.add_edge(START, "hotels")
b.add_edge("flights", END)
b.add_edge("hotels", END)
g = b.compile()

start = time.perf_counter()
out = asyncio.run(g.ainvoke({"results": []}))
elapsed = time.perf_counter() - start
assert sorted(out["results"]) == ["flights", "hotels"] and elapsed < 0.35
```

Use async nodes with async clients (httpx, async LLM SDKs) inside async services such as FastAPI, so one worker handles many concurrent runs. Never call blocking I/O inside an async node, because that stalls the event loop for every run on the worker.

## Likely follow-ups

- What happens if an async node calls `time.sleep` or a blocking HTTP client?

---

[← Q0568](../../batch_06_langgraph_langchain/0568_observability_for_langgraph_with_langsmith/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0570 →](../../batch_06_langgraph_langchain/0570_limit_parallelism_with_max_concurrency/README.md)

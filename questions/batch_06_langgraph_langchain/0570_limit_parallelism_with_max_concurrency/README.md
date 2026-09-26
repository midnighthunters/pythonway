# Q0570 · Limit parallelism with max_concurrency

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Concurrency | Medium |

## Question

Run a graph over many inputs with `batch`, but cap concurrency to respect a downstream rate limit. Measure the peak concurrency to prove the cap works.

## Answer

```python
import threading
import time
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

lock = threading.Lock()
active = {"now": 0, "peak": 0}


class State(TypedDict):
    doc: str
    label: str


def classify(state: State) -> dict:
    with lock:
        active["now"] += 1
        active["peak"] = max(active["peak"], active["now"])
    time.sleep(0.02)
    with lock:
        active["now"] -= 1
    return {"label": "contract" if "agreement" in state["doc"] else "other"}


b = StateGraph(State)
b.add_node("classify", classify)
b.add_edge(START, "classify")
b.add_edge("classify", END)
g = b.compile()
docs = [{"doc": f"agreement {i}" if i % 2 else f"memo {i}", "label": ""} for i in range(10)]
out = g.batch(docs, {"max_concurrency": 3})
assert [o["label"] for o in out[:2]] == ["other", "contract"] and len(out) == 10
assert 1 < active["peak"] <= 3
```

`max_concurrency` in the config also bounds parallel work inside a run (for example a wide `Send` fan-out). Set it from the downstream provider's rate limits, and combine it with the gateway's own quotas, so an evaluation batch can't starve production traffic.

## Likely follow-ups

- Where else would you enforce limits besides `max_concurrency`?

---

[← Q0569](../../batch_06_langgraph_langchain/0569_async_nodes_and_ainvoke/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0571 →](../../batch_06_langgraph_langchain/0571_timeouts_inside_nodes/README.md)

# Q0505 · Reducers and state channels

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Show the difference between overwrite keys and reducer keys in LangGraph state, using `operator.add` to accumulate a list of audit events across nodes.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    status: str
    audit: Annotated[list[str], operator.add]


def fetch(state: State) -> dict:
    return {"status": "fetched", "audit": ["fetched booking BK-9"]}


def rebook(state: State) -> dict:
    return {"status": "rebooked", "audit": ["rebooked on LH903"]}


b = StateGraph(State)
b.add_node("fetch", fetch)
b.add_node("rebook", rebook)
b.add_edge(START, "fetch")
b.add_edge("fetch", "rebook")
b.add_edge("rebook", END)
out = b.compile().invoke({"status": "new", "audit": ["run started"]})
assert out == {"status": "rebooked", "audit": ["run started", "fetched booking BK-9", "rebooked on LH903"]}
```

`status` has no reducer, so each write overwrites it. `audit` uses `operator.add`, so every node's list is appended. Choose reducers deliberately: accumulating keys (messages, results from parallel workers, audit logs) need reducers, while status-like keys should overwrite.

## Likely follow-ups

- What happens if two parallel nodes write `status` in the same step?

---

[← Q0504](../../batch_06_langgraph_langchain/0504_your_first_stategraph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0506 →](../../batch_06_langgraph_langchain/0506_custom_reducer_for_merging_dictionaries/README.md)

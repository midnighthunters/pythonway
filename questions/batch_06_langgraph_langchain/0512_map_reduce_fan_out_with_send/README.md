# Q0512 · Map-reduce fan-out with Send

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Use `Send` to process a variable number of documents in parallel (one worker invocation per document, each with its own input) and gather the results with a reducer.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class State(TypedDict):
    contracts: list[str]
    flags: Annotated[list[dict], operator.add]
    summary: str


class WorkerInput(TypedDict):
    contract: str


def fan_out(state: State) -> list[Send]:
    return [Send("review", {"contract": c}) for c in state["contracts"]]


def review(inp: WorkerInput) -> dict:
    text = inp["contract"]
    return {"flags": [{"contract": text.split(":")[0], "change_of_control": "change of control" in text}]}


def reduce_(state: State) -> dict:
    hits = sorted(f["contract"] for f in state["flags"] if f["change_of_control"])
    return {"summary": f"{len(hits)} of {len(state['flags'])} contracts have change-of-control clauses: {hits}"}


b = StateGraph(State)
b.add_node("review", review)
b.add_node("reduce", reduce_)
b.add_conditional_edges(START, fan_out, ["review"])
b.add_edge("review", "reduce")
b.add_edge("reduce", END)
out = b.compile().invoke({"contracts": ["C1: standard terms", "C2: change of control triggers consent",
                                        "C3: change of control clause"], "flags": [], "summary": ""})
assert out["summary"] == "2 of 3 contracts have change-of-control clauses: ['C2', 'C3']"
```

Each `Send` creates a separate invocation of `review` with its own private input (not the whole state). They run in parallel within one superstep, and the reducer gathers their outputs. Limit the fan-out width with `max_concurrency` in the config, and make sure failures in one branch are handled (a retry policy, or recording errors as results).

## Likely follow-ups

- How would you cap concurrency when fanning out to 500 documents?

---

[← Q0511](../../batch_06_langgraph_langchain/0511_update_and_route_with_command/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0513 →](../../batch_06_langgraph_langchain/0513_parallel_branches_and_supersteps/README.md)

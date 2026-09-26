# Q0506 · Custom reducer for merging dictionaries

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Write a custom reducer that deep-merges dictionary updates (so parallel workers can each contribute fields to a shared `findings` dict), and use it in a graph with two parallel branches.

## Answer

```python
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


def merge_findings(left: dict | None, right: dict | None) -> dict:
    out = dict(left or {})
    for key, value in (right or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge_findings(out[key], value)
        else:
            out[key] = value
    return out


class State(TypedDict):
    break_id: str
    findings: Annotated[dict, merge_findings]


def trade_checker(state: State) -> dict:
    return {"findings": {"trade": {"qty": 1000, "px": 101.20}}}


def confirm_checker(state: State) -> dict:
    return {"findings": {"confirm": {"qty": 1000, "px": 101.25}}}


def summarize(state: State) -> dict:
    f = state["findings"]
    return {"findings": {"diff": {"px": round(f["confirm"]["px"] - f["trade"]["px"], 4)}}}


b = StateGraph(State)
for name, fn in (("trade", trade_checker), ("confirm", confirm_checker), ("summarize", summarize)):
    b.add_node(name, fn)
b.add_edge(START, "trade")
b.add_edge(START, "confirm")
b.add_edge(["trade", "confirm"], "summarize")
b.add_edge("summarize", END)
out = b.compile().invoke({"break_id": "BRK-9", "findings": {}})
assert out["findings"] == {"trade": {"qty": 1000, "px": 101.2}, "confirm": {"qty": 1000, "px": 101.25},
                           "diff": {"px": 0.05}}
```

`add_edge(["trade", "confirm"], "summarize")` waits for both branches before running `summarize`. Reducers must be pure and deterministic, because they run during replays and time travel too. Test them as ordinary functions.

## Likely follow-ups

- Why must reducers be deterministic?

---

[← Q0505](../../batch_06_langgraph_langchain/0505_reducers_and_state_channels/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0507 →](../../batch_06_langgraph_langchain/0507_messagesstate_and_add_messages_semantics/README.md)

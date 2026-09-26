# Q0528 · Time travel: replay and fork

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Persistence | Hard |

## Question

Use the checkpoint history to go back to the state before a node ran, edit it, and fork a new execution from that point, leaving the original history intact.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    steps: Annotated[list[str], operator.add]


b = StateGraph(State)
b.add_node("plan", lambda s: {"steps": ["plan"]})
b.add_node("execute", lambda s: {"steps": ["execute"]})
b.add_edge(START, "plan")
b.add_edge("plan", "execute")
b.add_edge("execute", END)
app = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "tt-1"}}
app.invoke({"steps": []}, cfg)

history = list(app.get_state_history(cfg))
assert [h.next for h in history] == [(), ("execute",), ("plan",), ("__start__",)]
before_execute = next(h for h in history if h.next == ("execute",))
fork_cfg = app.update_state(before_execute.config, {"steps": ["human: add compliance check"]})
forked = app.invoke(None, fork_cfg)
assert forked["steps"] == ["plan", "human: add compliance check", "execute"]
assert len(list(app.get_state_history(cfg))) > len(history)
```

History is newest first. `update_state` on an old checkpoint creates a new branch (a new checkpoint whose parent is the old one), and invoking with `None` continues from there. The edit went through the `operator.add` reducer, so it was appended. Uses include debugging ("what if the planner had seen this?"), correcting a bad step without restarting, and reproducing incidents. Forking re-runs later nodes, so their side effects happen again: guard them with idempotency.

## Likely follow-ups

- Why is forking dangerous for nodes that send emails or payments?

---

[← Q0527](../../batch_06_langgraph_langchain/0527_inspect_state_snapshots/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0529 →](../../batch_06_langgraph_langchain/0529_correct_an_agent_with_update_state/README.md)

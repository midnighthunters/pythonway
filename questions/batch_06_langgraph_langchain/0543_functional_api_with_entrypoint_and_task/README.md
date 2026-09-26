# Q0543 · Functional API with entrypoint and task

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Functional API | Medium |

## Question

Write the same kind of workflow with LangGraph's functional API: `@task` for units of work (run in parallel via futures) and an `@entrypoint` with a checkpointer. Show that completed tasks aren't re-executed when the workflow resumes after an interrupt.

## Answer

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt

runs = {"quote": 0}


@task
def get_quote(supplier: str) -> float:
    runs["quote"] += 1
    return {"acme": 950.0, "globex": 910.0}[supplier]


@entrypoint(checkpointer=InMemorySaver())
def procurement(request: dict) -> dict:
    futures = [get_quote(s) for s in request["suppliers"]]
    quotes = {s: f.result() for s, f in zip(request["suppliers"], futures)}
    best = min(quotes, key=quotes.get)
    approved = interrupt({"approve_supplier": best, "price": quotes[best]})
    return {"supplier": best, "approved": approved, "quotes": quotes}


cfg = {"configurable": {"thread_id": "po-1"}}
paused = procurement.invoke({"suppliers": ["acme", "globex"]}, cfg)
assert runs["quote"] == 2
done = procurement.invoke(Command(resume=True), cfg)
assert done == {"supplier": "globex", "approved": True, "quotes": {"acme": 950.0, "globex": 910.0}}
assert runs["quote"] == 2
```

On resume, the entrypoint function re-runs from the top, but completed task results come from the checkpoint rather than being recomputed. That's why side effects belong inside tasks. The functional API suits code-shaped workflows (loops and ifs in plain Python). The Graph API suits explicit topologies you want to visualise and route.

## Likely follow-ups

- Why must side effects live inside tasks in the functional API?

---

[← Q0542](../../batch_06_langgraph_langchain/0542_durability_modes/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0544 →](../../batch_06_langgraph_langchain/0544_functional_api_versus_graph_api/README.md)

# Q0544 · Functional API versus Graph API

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Functional API | Easy |

## Question

When would you choose LangGraph's functional API over the Graph API, or the other way round?

## Answer

Functional API (`@entrypoint`, `@task`):
- It reads like normal Python: loops, conditionals, try/except. It is easy to add persistence, interrupts and streaming to existing code.
- State is local variables, so there's no schema or reducers to design.
- Good for linear or procedural workflows, and for migrating existing scripts to durable execution.

Graph API (`StateGraph`):
- Explicit nodes and edges that you can visualise, inspect and route (conditional edges, `Send`, `Command`).
- Shared, typed state with reducers. Good for complex topologies, multi-agent systems, parallel fan-out and when non-developers review the flow.
- Fine-grained streaming of node updates, and time travel at node granularity.

Both run on the same runtime (checkpointers, interrupts, streaming), and they can be mixed: a task can call a graph, and a graph node can call an entrypoint.

## Likely follow-ups

- Which would you choose for a 12-step approval workflow that risk reviewers must sign off on?

---

[← Q0543](../../batch_06_langgraph_langchain/0543_functional_api_with_entrypoint_and_task/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0545 →](../../batch_06_langgraph_langchain/0545_remaining_steps_for_graceful_stops/README.md)

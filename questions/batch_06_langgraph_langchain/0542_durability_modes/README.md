# Q0542 · Durability modes

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Persistence | Medium |

## Question

LangGraph lets you choose how eagerly checkpoints are written (for example `durability="sync"`, `"async"` or `"exit"`). What's the trade-off?

## Answer

- `sync`: the checkpoint is written before the next step starts. It is the most durable (a crash loses at most the in-progress step), but adds write latency to every step.
- `async`: checkpoints are written in the background while the next step runs. Throughput is good, but a crash at the wrong moment can lose the last checkpoint(s).
- `exit`: state is persisted only when the run finishes or pauses (interrupt or error). It is the fastest, but intermediate progress is lost on a crash, and time travel over intermediate steps is limited.

Choose per workload:
- Long-running or side-effecting agents (bookings, payments): `sync`, together with idempotent side effects.
- Interactive chat, where speed matters and steps are cheap to redo: `async`.
- Short, stateless batch pipelines: `exit`.

Pass it per run (`graph.invoke(inputs, config, durability="sync")`), and measure the latency impact against your checkpointer.

## Likely follow-ups

- Which mode would you use for a trade-remediation agent, and why?

---

[← Q0541](../../batch_06_langgraph_langchain/0541_cache_expensive_nodes_with_cachepolicy/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0543 →](../../batch_06_langgraph_langchain/0543_functional_api_with_entrypoint_and_task/README.md)

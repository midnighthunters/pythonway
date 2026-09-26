# Q0591 · Performance tuning for LangGraph apps

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Performance | Medium |

## Question

A LangGraph agent is slow and expensive. Where do you look, and what can you change?

## Answer

Measure first: per-node latency and token usage from traces, the number of supersteps per run, and checkpoint write time.

Common fixes:
- Fewer model calls: collapse unnecessary agent hops, use deterministic nodes for fixed steps, and plan once instead of ReAct-style planning at every step where possible.
- Smaller or faster models for routing, extraction and summaries, and larger ones only where evaluations show a need.
- Parallelism: run independent branches concurrently (parallel edges, `Send`), use async nodes with async clients, and parallel tool calls.
- Context size: trim or summarise history, compact tool outputs, load only the relevant tools, and use prompt caching (a stable prefix).
- Caching: `CachePolicy` on deterministic nodes, and caching of embeddings and retrieval results.
- Checkpoint overhead: choose the durability mode per workload, keep the state small, and use a fast, well-indexed Postgres with connection pooling.
- Streaming: stream tokens and progress, so perceived latency drops even when total time doesn't.
- Serving: enough workers, autoscaling on concurrency, and co-location with the gateway and models.

## Likely follow-ups

- Which of these fixes risks changing the agent's behaviour, and how would you check?

---

[← Q0590](../../batch_06_langgraph_langchain/0590_state_design_anti_patterns/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0592 →](../../batch_06_langgraph_langchain/0592_securing_a_langgraph_deployment/README.md)

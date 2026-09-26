# Q0464 · Stateless versus stateful agent services

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Architecture | Medium |

## Question

Should an agent service keep conversation and run state in memory, or be stateless with external state? Discuss the trade-offs.

## Answer

- In-memory stateful services are simple and fast, but state is lost on crash or deploy, you need sticky routing, they're hard to scale horizontally, and long waits (approvals) tie up processes.
- Stateless services with external state (a checkpointer in Postgres, Redis or Cosmos DB, keyed by thread or run id): any replica can serve any request, they survive restarts and deployments, autoscale freely, and support long pauses. The costs are latency and cost of state reads and writes, serialisation, and schema versioning.

Practical design: stateless API and worker pods, durable checkpoints after each step, caches for hot state, and streaming connections routed to whichever pod is running the step (clients reconnect with a thread id). This mirrors the direction of MCP's 2026-07-28 revision, which removed protocol-level sessions in favour of explicit state handles.

## Likely follow-ups

- How do you resume a streamed response after the pod serving it dies?

---

[← Q0463](../../batch_05_agentic_patterns_orchestration/0463_choosing_an_agent_framework/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0465 →](../../batch_05_agentic_patterns_orchestration/0465_stream_agent_progress_events/README.md)

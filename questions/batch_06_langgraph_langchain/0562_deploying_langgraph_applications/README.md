# Q0562 · Deploying LangGraph applications

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Deployment | Medium |

## Question

What are the options for deploying LangGraph agents in production, and what does a self-hosted deployment need?

## Answer

Options:
- LangGraph Platform or Server (managed cloud, hybrid, or self-hosted containers): it provides an HTTP API for assistants, threads and runs, persistence (Postgres), a task queue for background runs, streaming endpoints, cron jobs, double-texting handling, authentication hooks, and Studio for debugging.
- Your own service: embed compiled graphs in FastAPI workers with a Postgres checkpointer, your own queue for long runs (SQS, Service Bus or Celery), and SSE or WebSocket streaming.

A self-hosted setup needs:
- Stateless API and worker containers on Kubernetes or ECS, with autoscaling on queue depth or concurrency.
- A durable checkpointer and store (Postgres), with backups, encryption and connection pooling.
- A task queue for background and long runs, with idempotent run starts.
- Secrets management for model and tool credentials, and private networking to the LLM gateway.
- Observability (OpenTelemetry or LangSmith), rate limiting, auth, and per-tenant quotas.
- A CI/CD pipeline with evaluation gates, and versioned graph deployments that handle in-flight threads.

## Likely follow-ups

- What would push you to the managed platform rather than self-hosting, in a bank?

---

[← Q0561](../../batch_06_langgraph_langchain/0561_thread_ids_and_multi_user_safety/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0563 →](../../batch_06_langgraph_langchain/0563_assistants_threads_and_runs/README.md)

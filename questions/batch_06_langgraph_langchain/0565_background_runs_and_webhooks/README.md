# Q0565 · Background runs and webhooks

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph Server | Medium |

## Question

How should long-running agent tasks (minutes to hours) be run and reported without holding an HTTP connection open?

## Answer

- Start a background run: the API returns a run id immediately (202 Accepted), and a worker picks the run up from a durable queue.
- Progress: clients poll the run status or thread state, subscribe to a stream they can reconnect to (keyed by run id), or receive webhooks.
- Webhooks on completion: the server POSTs the result to a registered URL. Sign the payloads (HMAC), include an idempotency id, retry with backoff, and let receivers verify the signature and timestamp.
- Interrupts: a background run that needs approval enters an interrupted state. Notify the approver (email, Teams), and resume it through the API when they decide.
- Reliability: runs survive worker restarts via checkpoints, have timeouts and cancellation, and use at-least-once processing with idempotent steps.

This is the pattern for event-driven agents (disruption recovery, CI code fixes, trade-break remediation) where no user is waiting on the page.

## Likely follow-ups

- How should a webhook receiver protect itself against forged or replayed calls?

---

[← Q0564](../../batch_06_langgraph_langchain/0564_double_texting_strategies/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0566 →](../../batch_06_langgraph_langchain/0566_cron_jobs_for_agents/README.md)

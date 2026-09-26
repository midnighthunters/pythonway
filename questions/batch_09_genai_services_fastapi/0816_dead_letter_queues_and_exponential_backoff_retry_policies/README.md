# Q0816 · Dead Letter Queues and exponential backoff retry policies

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

How does a Dead Letter Queue (DLQ) isolate poison-pill messages in an agent processing pipeline? What retry policies protect downstream AI providers?

## Answer

Poison-Pill Problem:
An agent job with corrupted input or unparseable formatting crashes the worker. If re-queued immediately, it crashes another worker, looping infinitely and consuming 100% of queue capacity.

DLQ Architecture:
1. Max Receive Count: A message is allowed up to $N$ retry attempts (e.g. $N=3$).
2. Exponential Backoff with Jitter: If an external cloud LLM returns 500, the message visibility timeout increases exponentially (10s -> 40s -> 160s) before retry.
3. Dead Letter Queue Transfer:
   - If the message fails $N$ times, the queue broker moves it to an isolated Dead Letter Queue (DLQ).
   - An alert notifies operations engineers, who inspect the failure payload without impacting live traffic.

## Likely follow-ups

- How do you replay messages from a DLQ once a downstream bug is patched?
- What metrics indicate that a DLQ is accumulating poison-pill messages?

---

[← Q0815](../../batch_09_genai_services_fastapi/0815_idempotency_keys_in_message_queue_consumers/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0817 →](../../batch_09_genai_services_fastapi/0817_worker_concurrency_and_graceful_shutdown_on_sigterm/README.md)

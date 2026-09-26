# Q0814 · Distributed message queues: Celery, ARQ, and Redis Queue for agents

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Compare distributed message queue architectures (Celery, ARQ, Redis Queue, AWS SQS) for hosting long-running Python agent workers.

## Answer

Comparison for GenAI Microservices:

1. Celery:
   - Strengths: Mature, battle-tested, rich feature set (rate limiting, retries, canvases, workflows, multiple brokers).
   - Drawbacks: Heavyweight, complex configuration, historically synchronous (asyncio support requires extra care with event loops).
2. ARQ (Async Redis Queue):
   - Strengths: Built natively for Python `asyncio` and Redis. Lightweight, fast, seamlessly handles coroutine jobs and streaming I/O.
   - Ideal Fit: Modern FastAPI applications executing async LangGraph workflows.
3. AWS SQS / Azure Service Bus:
   - Strengths: Fully managed cloud serverless queues. Infinite scale, at-least-once delivery, integrated Dead Letter Queues (DLQ), zero infrastructure management.
   - Ideal Fit: Multi-region enterprise banking architectures.

## Likely follow-ups

- How does ARQ's native asyncio support prevent worker thread starvation compared to traditional Celery?
- How is task serialization (JSON vs Pickle) governed in enterprise security standards?

---

[← Q0813](../../batch_09_genai_services_fastapi/0813_background_task_processing_with_fastapi_backgroundtasks/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0815 →](../../batch_09_genai_services_fastapi/0815_idempotency_keys_in_message_queue_consumers/README.md)

# Q0818 · Storing conversation history in NoSQL: DynamoDB and Cosmos DB

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Design a NoSQL schema in Amazon DynamoDB or Azure Cosmos DB for multi-tenant conversational agent history, specifying Partition Key, Sort Key, and TTL.

## Answer

Relational databases struggle with massive multi-turn conversation growth. A high-throughput NoSQL key-value / document database provides single-digit millisecond latency and horizontal scaling.

Schema Design:
- Partition Key (`PK`): `TENANT#{tenant_id}#THREAD#{thread_id}`
  - Groups all turns for a specific conversation thread onto a single physical database partition.
- Sort Key (`SK`): `MSG#{timestamp_iso8601}#{message_id}`
  - Allows querying chronological message history using standard range queries (`SK > MSG#2026-09-26T00:00:00Z`).
- Attributes:
  - `role`: `"user"` | `"assistant"` | `"tool"`
  - `content`: Message text or structured payload.
  - `tokens`: Prompt/completion token count.
  - `model_version`: Model identifier.
- Time To Live (`TTL`):
  - Unix epoch timestamp (e.g. `now + 90 days`). DynamoDB automatically purges expired messages in the background at zero write cost.

## Likely follow-ups

- How does this partition key design prevent "hot partition" bottlenecks during viral traffic?
- What Global Secondary Index (GSI) allows querying all active threads belonging to a specific user?

---

[← Q0817](../../batch_09_genai_services_fastapi/0817_worker_concurrency_and_graceful_shutdown_on_sigterm/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0819 →](../../batch_09_genai_services_fastapi/0819_dynamodb_thread_history_repository_implementation_in_python/README.md)

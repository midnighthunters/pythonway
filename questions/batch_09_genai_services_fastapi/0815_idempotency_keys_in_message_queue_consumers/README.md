# Q0815 · Idempotency keys in message queue consumers

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code for an asynchronous queue worker that uses an idempotency key to prevent executing duplicate financial transactions during message retries.

## Answer

In distributed messaging queues (SQS, Kafka, RabbitMQ), network partitions cause at-least-once delivery: the same message can be delivered twice. Workers must enforce idempotency.

```python
from typing import Any, Dict, Set


class IdempotentMessageConsumer:
    def __init__(self):
        self._processed_keys: Set[str] = set()
        self.processed_records: Dict[str, Any] = {}

    def process_message(self, idempotency_key: str, payload: Dict[str, Any]) -> bool:
        if idempotency_key in self._processed_keys:
            # Duplicate message detected; acknowledge queue without re-executing
            return False

        # Execute business logic (e.g. fund settlement)
        tx_id = payload["transaction_id"]
        self.processed_records[tx_id] = payload["amount"]

        # Record idempotency key atomically
        self._processed_keys.add(idempotency_key)
        return True


consumer = IdempotentMessageConsumer()
msg = {"transaction_id": "TX-100", "amount": 50000.0}

# First delivery: processed
assert consumer.process_message("idem-uuid-001", msg) is True
assert consumer.processed_records["TX-100"] == 50000.0

# Second delivery of duplicate message: skipped safely
assert consumer.process_message("idem-uuid-001", msg) is False
assert len(consumer.processed_records) == 1
```

## Likely follow-ups

- How long should idempotency keys be retained in Redis before TTL expiration?
- What happens if the worker crashes after executing the action but before committing the idempotency key?

---

[← Q0814](../../batch_09_genai_services_fastapi/0814_distributed_message_queues_celery_arq_and_redis_queue_for/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0816 →](../../batch_09_genai_services_fastapi/0816_dead_letter_queues_and_exponential_backoff_retry_policies/README.md)

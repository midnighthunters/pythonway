# Q0883 · Exactly-once processing versus at-least-once processing in agent task queues

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Hard |

## Question

Explain why distributed message queues provide at-least-once delivery by default, and write Python code implementing an idempotency gate to achieve effective exactly-once execution.

## Answer

In distributed networks, worker acknowledgments (`ACK`) can be dropped due to network partitions or worker crashes. The message broker redelivers the message to another worker.

Without an idempotency gate, side-effect operations (e.g. sending a trade notification email or charging a client account) execute multiple times.

An **Idempotency Gate** checks a distributed database (e.g. DynamoDB/Redis) using an atomic conditional write (`SETNX` or `attribute_not_exists`) before processing.

```python
from typing import Dict, Optional, Tuple


class IdempotencyGate:
    def __init__(self):
        # Maps message_id -> status ('PROCESSING', 'COMPLETED')
        self.registry: Dict[str, str] = {}

    def try_acquire(self, message_id: str) -> bool:
        # Atomic check-and-set
        if message_id in self.registry:
            return False
        self.registry[message_id] = "PROCESSING"
        return True

    def mark_completed(self, message_id: str) -> None:
        self.registry[message_id] = "COMPLETED"


gate = IdempotencyGate()

# First attempt by Worker A succeeds
assert gate.try_acquire("msg_001") is True
gate.mark_completed("msg_001")

# Second redelivery attempt by Worker B is dropped
assert gate.try_acquire("msg_001") is False
```

## Likely follow-ups

- What happens if Worker A crashes while status is `PROCESSING` (deadlock without TTL)?
- Why does the two generals' problem prove that true physical exactly-once delivery is impossible?

---

[← Q0882](../../batch_09_genai_services_fastapi/0882_s3_large_payload_offloading_pattern_for_message_queues/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0884 →](../../batch_09_genai_services_fastapi/0884_throttling_worker_consumption_to_match_downstream_cloud_api/README.md)

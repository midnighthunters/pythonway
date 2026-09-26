# Q0452 · Queue-triggered agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Event-driven agents | Medium |

## Question

Implement an agent worker that consumes messages from a queue: deduplicate by message id (at-least-once delivery), retry failures, and move a message to a dead-letter queue after N failed attempts.

## Answer

```python
from collections import deque
from typing import Callable


def run_worker(queue: deque, handle: Callable[[dict], None], max_attempts: int = 3) -> dict:
    processed: set[str] = set()
    dlq, attempts = [], {}
    while queue:
        msg = queue.popleft()
        if msg["id"] in processed:
            continue
        try:
            handle(msg)
            processed.add(msg["id"])
        except Exception as e:
            attempts[msg["id"]] = attempts.get(msg["id"], 0) + 1
            if attempts[msg["id"]] >= max_attempts:
                dlq.append({**msg, "error": str(e)})
            else:
                queue.append(msg)
    return {"processed": sorted(processed), "dlq": dlq}


handled: list[str] = []


def handle(msg: dict) -> None:
    if msg["body"] == "poison":
        raise ValueError("unparseable break record")
    handled.append(msg["id"])


q = deque([{"id": "m1", "body": "break BRK-1"}, {"id": "m2", "body": "poison"}, {"id": "m1", "body": "break BRK-1"},
           {"id": "m3", "body": "break BRK-3"}])
out = run_worker(q, handle)
assert out["processed"] == ["m1", "m3"] and handled == ["m1", "m3"]
assert out["dlq"][0]["id"] == "m2" and "unparseable" in out["dlq"][0]["error"]
```

The duplicate delivery of m1 is ignored. Real brokers (SQS, Service Bus, Kafka consumer groups) handle redelivery and dead-lettering. Your job is idempotent handling (a persisted processed-id store, or idempotency keys downstream), visibility timeouts longer than the agent run, and DLQ monitoring with a replay tool.

## Likely follow-ups

- What goes wrong if the visibility timeout is shorter than the agent's run time?

---

[← Q0451](../../batch_05_agentic_patterns_orchestration/0451_perceive_act_verify_loop/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0453 →](../../batch_05_agentic_patterns_orchestration/0453_scheduled_and_background_agents/README.md)

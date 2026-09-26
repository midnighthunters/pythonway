# Q0423 · Idempotency keys for tool calls

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Reliability | Medium |

## Question

Agents retry. Implement an idempotency layer for a write tool: the same key with the same payload returns the original result without re-executing; the same key with a different payload is rejected as a conflict.

## Answer

```python
import hashlib
import json
from typing import Callable


class IdempotencyConflict(Exception):
    pass


class IdempotentExecutor:
    def __init__(self) -> None:
        self._store: dict[str, tuple[str, object]] = {}

    def execute(self, key: str, payload: dict, fn: Callable[[dict], object]) -> object:
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        if key in self._store:
            stored_digest, result = self._store[key]
            if stored_digest != digest:
                raise IdempotencyConflict(f"key {key} reused with a different payload")
            return result
        result = fn(payload)
        self._store[key] = (digest, result)
        return result


transfers: list[dict] = []


def transfer(p: dict) -> str:
    transfers.append(p)
    return f"TX-{len(transfers)}"


ex = IdempotentExecutor()
p = {"from": "ACC-1", "to": "ACC-2", "amount": "250.00"}
assert ex.execute("run42-step3", p, transfer) == "TX-1"
assert ex.execute("run42-step3", dict(reversed(list(p.items()))), transfer) == "TX-1"
assert len(transfers) == 1
try:
    ex.execute("run42-step3", {**p, "amount": "2500.00"}, transfer)
    raise AssertionError
except IdempotencyConflict:
    pass
```

Derive keys from the run id plus the step (not from the model's output), so a retried step reuses its key. In production, store the keys in a database with a unique constraint and a TTL, record in-progress status to handle concurrent duplicates, and pass the key through to downstream APIs that support it (many payment APIs do).

## Likely follow-ups

- How do you handle two concurrent requests with the same key?

---

[← Q0422](../../batch_05_agentic_patterns_orchestration/0422_saga_pattern_for_multi_step_bookings/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0424 →](../../batch_05_agentic_patterns_orchestration/0424_retry_with_exponential_backoff_and_jitter/README.md)

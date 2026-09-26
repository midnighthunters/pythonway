# Q0424 · Retry with exponential backoff and jitter

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Reliability | Medium |

## Question

Implement a retry helper for transient errors (429, timeouts) with capped exponential backoff and full jitter, using injectable sleep and random functions so it's testable, and honouring a server-provided `retry_after` hint.

## Answer

```python
import random
from typing import Callable


class Retryable(Exception):
    def __init__(self, msg: str, retry_after: float | None = None) -> None:
        super().__init__(msg)
        self.retry_after = retry_after


def retry(fn: Callable[[], object], attempts: int = 5, base: float = 0.5, cap: float = 8.0,
          sleep: Callable[[float], None] = lambda s: None, rng: random.Random | None = None):
    rng = rng or random.Random()
    for attempt in range(attempts):
        try:
            return fn()
        except Retryable as e:
            if attempt == attempts - 1:
                raise
            delay = e.retry_after if e.retry_after is not None else rng.uniform(0, min(cap, base * 2 ** attempt))
            sleep(delay)


calls, sleeps = [0], []


def flaky():
    calls[0] += 1
    if calls[0] == 1:
        raise Retryable("429", retry_after=2.0)
    if calls[0] < 4:
        raise Retryable("timeout")
    return "ok"


assert retry(flaky, sleep=sleeps.append, rng=random.Random(0)) == "ok"
assert calls[0] == 4 and sleeps[0] == 2.0 and all(0 <= s <= 8 for s in sleeps[1:]) and len(sleeps) == 3
try:
    retry(lambda: (_ for _ in ()).throw(Retryable("always")), attempts=2, sleep=sleeps.append)
    raise AssertionError
except Retryable:
    pass
```

Full jitter spreads retries out, which avoids thundering herds when many agents hit the same 429 at once. Only retry idempotent operations (or ones protected by idempotency keys), cap the total retry time within the request deadline, and count retries as a metric.

## Likely follow-ups

- Why is retrying a non-idempotent payment call dangerous without idempotency keys?

---

[← Q0423](../../batch_05_agentic_patterns_orchestration/0423_idempotency_keys_for_tool_calls/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0425 →](../../batch_05_agentic_patterns_orchestration/0425_circuit_breaker_for_flaky_tools/README.md)

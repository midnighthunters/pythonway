# Q0385 · Rate-limit evaluation traffic with a token bucket

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation infrastructure | Medium |

## Question

Evaluation runs must not exceed a tokens-per-minute quota shared with production. Implement a token bucket with an injectable clock that tells callers how long to wait before a request of a given token size.

## Answer

```python
class TokenBucket:
    def __init__(self, capacity: float, refill_per_s: float, clock) -> None:
        self.capacity, self.rate, self.clock = capacity, refill_per_s, clock
        self.tokens = capacity
        self.last = clock()

    def _refill(self) -> None:
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now

    def try_acquire(self, amount: float) -> float:
        """Returns 0 if acquired now, otherwise seconds to wait before retrying."""
        if amount > self.capacity:
            raise ValueError("request larger than bucket capacity")
        self._refill()
        if self.tokens >= amount:
            self.tokens -= amount
            return 0.0
        return (amount - self.tokens) / self.rate


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


clock = FakeClock()
bucket = TokenBucket(capacity=60_000, refill_per_s=1_000, clock=clock)
assert bucket.try_acquire(50_000) == 0.0
assert bucket.try_acquire(20_000) == 10.0
clock.t = 10.0
assert bucket.try_acquire(20_000) == 0.0
```

That is a 60k tokens-per-minute quota, refilling at 1k per second. Budget with the estimated tokens (prompt plus `max_tokens`) before the call, then reconcile with the actual usage. Give evaluations their own lower-priority quota share, or a separate deployment, so they never cause production 429s.

## Likely follow-ups

- How would you share one bucket across several evaluation worker processes?

---

[← Q0384](../../batch_04_llm_evaluation_observability/0384_load_test_an_llm_endpoint/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0386 →](../../batch_04_llm_evaluation_observability/0386_reproducible_evaluations/README.md)

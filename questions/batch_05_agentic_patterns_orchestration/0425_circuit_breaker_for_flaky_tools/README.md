# Q0425 · Circuit breaker for flaky tools

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Reliability | Medium |

## Question

Implement a circuit breaker with closed, open and half-open states: open after N consecutive failures, fail fast while open, allow one trial call after a cool-down, and close again on success. Use an injectable clock.

## Answer

```python
class CircuitOpen(Exception):
    pass


class CircuitBreaker:
    def __init__(self, threshold: int, cooldown: float, clock) -> None:
        self.threshold, self.cooldown, self.clock = threshold, cooldown, clock
        self.failures = 0
        self.state = "closed"
        self.opened_at = 0.0

    def call(self, fn):
        if self.state == "open":
            if self.clock() - self.opened_at < self.cooldown:
                raise CircuitOpen("tool temporarily unavailable")
            self.state = "half_open"
        try:
            result = fn()
        except Exception:
            self.failures += 1
            if self.state == "half_open" or self.failures >= self.threshold:
                self.state, self.opened_at = "open", self.clock()
            raise
        self.failures, self.state = 0, "closed"
        return result


t = [0.0]
cb = CircuitBreaker(threshold=2, cooldown=30, clock=lambda: t[0])


def boom():
    raise ConnectionError("down")


for _ in range(2):
    try:
        cb.call(boom)
    except ConnectionError:
        pass
assert cb.state == "open"
try:
    cb.call(lambda: "never runs")
    raise AssertionError
except CircuitOpen:
    pass
t[0] = 31
assert cb.call(lambda: "recovered") == "recovered" and cb.state == "closed"
```

For agents, return `CircuitOpen` to the model as a structured, non-retryable error ("the FX service is unavailable; proceed without it or tell the user"), so it adapts instead of hammering a dead dependency. Keep a breaker per downstream dependency, and expose its state as a metric.

## Likely follow-ups

- What should happen in half-open state if several requests arrive at once?

---

[← Q0424](../../batch_05_agentic_patterns_orchestration/0424_retry_with_exponential_backoff_and_jitter/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0426 →](../../batch_05_agentic_patterns_orchestration/0426_timeouts_and_cancellation_in_agent_runs/README.md)

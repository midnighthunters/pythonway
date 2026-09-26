# Q0850 · Circuit breaker pattern for downstream LLM provider outages

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Hard |

## Question

Implement a production-grade Circuit Breaker in Python with states CLOSED, OPEN, and HALF_OPEN to protect GenAI services during model provider downtime.

## Answer

When Azure OpenAI or AWS Bedrock suffers an outage, continuing to hammer the API causes thread exhaustion and slow user timeouts. A Circuit Breaker trips to `OPEN` after a consecutive failure threshold, failing fast immediately without making network calls, before testing recovery in `HALF_OPEN` state.

```python
import time
from typing import Callable


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time_sec: float = 1.0):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.consecutive_failures = 0
        self.last_failure_time = 0.0

    def call(self, func: Callable, *args, **kwargs):
        now = time.time()

        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_time_sec:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit is OPEN: failing fast")

        try:
            result = func(*args, **kwargs)
            # Success in CLOSED or HALF_OPEN
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.consecutive_failures = 0
            return result
        except Exception as e:
            self.consecutive_failures += 1
            self.last_failure_time = now
            if self.consecutive_failures >= self.failure_threshold:
                self.state = "OPEN"
            raise e


# Verification
cb = CircuitBreaker(failure_threshold=2, recovery_time_sec=0.1)


def failing_llm_call():
    raise ConnectionError("503 Service Unavailable")


# Call 1 fails
try:
    cb.call(failing_llm_call)
except ConnectionError:
    pass
assert cb.state == "CLOSED"

# Call 2 fails -> trips breaker to OPEN
try:
    cb.call(failing_llm_call)
except ConnectionError:
    pass
assert cb.state == "OPEN"

# Immediate call fails fast with CircuitBreakerOpenException without invoking func
try:
    cb.call(failing_llm_call)
    assert False, "Should have raised CircuitBreakerOpenException"
except CircuitBreakerOpenException:
    pass
```

## Likely follow-ups

- How does the fallback handler provide a graceful degraded response (e.g. cached answer or local model)?
- How do you aggregate circuit breaker metrics across multiple Kubernetes pods?

---

[← Q0849](../../batch_09_genai_services_fastapi/0849_priority_queues_for_tier_1_bank_workloads_versus_batch/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0851 →](../../batch_09_genai_services_fastapi/0851_adaptive_rate_limiting_based_on_upstream_error_rates_and/README.md)

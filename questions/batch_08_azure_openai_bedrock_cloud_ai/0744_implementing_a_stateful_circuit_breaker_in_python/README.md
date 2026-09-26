# Q0744 · Implementing a stateful Circuit Breaker in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Write Python code implementing a stateful Circuit Breaker with failure thresholds and recovery probe logic for an LLM API client.

## Answer

```python
import time
from typing import Callable


class LLMCircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time_seconds: float = 1.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time_seconds
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = 0.0

    def execute(self, api_fn: Callable[[], str]) -> str:
        now = time.time()

        if self.state == "OPEN":
            if now - self.last_failure_time >= self.recovery_time:
                self.state = "HALF_OPEN"
            else:
                raise RuntimeError("CircuitBreaker is OPEN: Fast-failing request")

        try:
            res = api_fn()
            # Success in CLOSED or HALF_OPEN
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return res
        except Exception as exc:
            self.failure_count += 1
            self.last_failure_time = now
            if self.failure_count >= self.failure_threshold or self.state == "HALF_OPEN":
                self.state = "OPEN"
            raise exc


cb = LLMCircuitBreaker(failure_threshold=2, recovery_time_seconds=0.05)


def failing_call():
    raise ConnectionResetError("Cloud AI 503 Service Unavailable")


# 2 failures trip breaker
for _ in range(2):
    try:
        cb.execute(failing_call)
    except Exception:
        pass

assert cb.state == "OPEN"

# Immediate fast-fail without calling endpoint
try:
    cb.execute(failing_call)
    assert False, "Should raise fast-fail"
except RuntimeError as err:
    assert "CircuitBreaker is OPEN" in str(err)

# Wait for recovery period
time.sleep(0.06)
# Half-open probe succeeds
ok = cb.execute(lambda: "Recovered output")
assert ok == "Recovered output"
assert cb.state == "CLOSED"
```

## Likely follow-ups

- How does a circuit breaker track errors across multiple parallel worker threads?
- What metrics should be emitted to Grafana when a circuit breaker changes state?

---

[← Q0743](../../batch_08_azure_openai_bedrock_cloud_ai/0743_circuit_breaker_pattern_for_failing_cloud_ai_endpoints/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0745 →](../../batch_08_azure_openai_bedrock_cloud_ai/0745_per_tenant_rate_limiting_with_sliding_window_in_python/README.md)

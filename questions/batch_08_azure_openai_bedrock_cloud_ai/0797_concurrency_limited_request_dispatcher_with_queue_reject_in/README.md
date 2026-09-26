# Q0797 · Concurrency-limited request dispatcher with queue reject in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Hard |

## Question

Write Python code implementing a concurrency-limited request dispatcher that accepts requests up to a max worker cap, queues a bounded number of requests, and rejects excess load.

## Answer

```python
import threading
from typing import Callable


class ConcurrencyGovernor:
    def __init__(self, max_concurrent: int = 2, max_queue: int = 2):
        self.max_concurrent = max_concurrent
        self.max_queue = max_queue
        self.active_count = 0
        self.queued_count = 0
        self._lock = threading.Lock()

    def execute(self, task_fn: Callable[[], str]) -> str:
        with self._lock:
            if self.active_count < self.max_concurrent:
                self.active_count += 1
                admitted = True
            elif self.queued_count < self.max_queue:
                self.queued_count += 1
                admitted = False
            else:
                raise RuntimeError("HTTP 503 Load Shed: Concurrency and queue capacity exhausted")

        # Simulate execution
        try:
            return task_fn()
        finally:
            with self._lock:
                if admitted:
                    self.active_count -= 1
                else:
                    self.queued_count -= 1


governor = ConcurrencyGovernor(max_concurrent=1, max_queue=1)

# Task 1 active
t1 = governor.execute(lambda: "Task 1 complete")
assert t1 == "Task 1 complete"

# Test rejection when limits saturated
gov_tight = ConcurrencyGovernor(max_concurrent=0, max_queue=0)
try:
    gov_tight.execute(lambda: "Never runs")
    assert False, "Should raise load shed error"
except RuntimeError as err:
    assert "Load Shed" in str(err)
```

## Likely follow-ups

- How does adaptive concurrency control (e.g. Netflix concurrency-limits) dynamically tune `max_concurrent`?
- How should rejected requests be attributed in tenant SLA reporting?

---

[← Q0796](../../batch_08_azure_openai_bedrock_cloud_ai/0796_load_shedding_under_extreme_cloud_ai_gateway_concurrency/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0798 →](../../batch_08_azure_openai_bedrock_cloud_ai/0798_audit_trail_persistence_to_immutable_storage/README.md)

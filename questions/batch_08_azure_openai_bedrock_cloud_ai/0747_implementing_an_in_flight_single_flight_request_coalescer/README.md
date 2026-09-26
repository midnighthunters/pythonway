# Q0747 · Implementing an in-flight single-flight request coalescer

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Hard |

## Question

Write Python code implementing a thread-safe single-flight request coalescer that deduplicates identical concurrent LLM executions.

## Answer

```python
import threading
import time
from typing import Any, Callable, Dict


class SingleFlightCoalescer:
    def __init__(self):
        self._lock = threading.Lock()
        self._in_flight: Dict[str, Any] = {}
        self.execution_count = 0

    def execute(self, key: str, fn: Callable[[], str]) -> str:
        with self._lock:
            if key in self._in_flight:
                event, result_box = self._in_flight[key]
                # Wait for running execution
                wait_needed = True
            else:
                event = threading.Event()
                result_box = {}
                self._in_flight[key] = (event, result_box)
                wait_needed = False

        if wait_needed:
            event.wait()
            return result_box["value"]

        # Run primary execution
        try:
            self.execution_count += 1
            res = fn()
            result_box["value"] = res
        finally:
            with self._lock:
                event.set()
                del self._in_flight[key]

        return res


coalescer = SingleFlightCoalescer()


def slow_llm_call():
    time.sleep(0.05)
    return "Market analysis complete."


# Simulate 2 concurrent callers with same prompt key
results = []


def worker():
    results.append(coalescer.execute("prompt_hash_1", slow_llm_call))


t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=worker)
t1.start()
t2.start()
t1.join()
t2.join()

assert len(results) == 2
assert results[0] == "Market analysis complete."
assert results[1] == "Market analysis complete."
assert coalescer.execution_count == 1  # Only executed once!
```

## Likely follow-ups

- What happens if the primary execution thread raises an unhandled exception?
- How should timeouts be applied to waiting subscribers?

---

[← Q0746](../../batch_08_azure_openai_bedrock_cloud_ai/0746_request_deduplication_for_identical_in_flight_prompts/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0748 →](../../batch_08_azure_openai_bedrock_cloud_ai/0748_health_checks_and_canary_deployments_for_llm_services/README.md)

# Q0879 · Handling unhandled worker exceptions and capturing crash stack traces in DLQs

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code that intercepts unhandled worker exceptions during agent execution, formats full tracebacks, and moves the poisoned message to a Dead Letter Queue (DLQ).

## Answer

Crashing a worker without capturing the exception loses critical debugging telemetry. The exception handler must catch `Exception`, capture the traceback, increment failure counts, and write the dead message to a DLQ for manual developer replay.

```python
import traceback
from typing import Dict, List


class WorkerExecutionPipeline:
    def __init__(self):
        self.dlq: List[Dict] = []
        self.success_store: List[Dict] = []

    def execute_task(self, task_id: str, payload: dict, handler_fn) -> bool:
        try:
            result = handler_fn(payload)
            self.success_store.append({"task_id": task_id, "result": result})
            return True
        except Exception as e:
            # Capture full traceback for DLQ
            tb = traceback.format_exc()
            dlq_record = {
                "task_id": task_id,
                "payload": payload,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": tb,
            }
            self.dlq.append(dlq_record)
            return False


pipeline = WorkerExecutionPipeline()


def faulty_task(payload: dict):
    if "corrupted" in payload:
        raise ValueError("Corrupted financial input matrix")
    return "OK"


# Good task
assert pipeline.execute_task("t1", {"data": 123}, faulty_task) is True
assert len(pipeline.success_store) == 1

# Poisoned task
assert pipeline.execute_task("t2", {"corrupted": True}, faulty_task) is False
assert len(pipeline.dlq) == 1
assert pipeline.dlq[0]["error_type"] == "ValueError"
assert "Corrupted financial input matrix" in pipeline.dlq[0]["error_message"]
```

## Likely follow-ups

- How do you implement DLQ redrive mechanisms once the bug is resolved?
- What alerting threshold should trigger PagerDuty when DLQ depth rises?

---

[← Q0878](../../batch_09_genai_services_fastapi/0878_worker_memory_leak_mitigation_recycling_worker_processes/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0880 →](../../batch_09_genai_services_fastapi/0880_scheduling_recurring_batch_embedding_updates_with_celery/README.md)

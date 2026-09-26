# Q0817 · Worker concurrency and graceful shutdown on SIGTERM

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Hard |

## Question

Write Python code demonstrating a graceful worker loop that traps `SIGTERM` / `SIGINT` signals, finishes processing the current in-flight agent job, and shuts down cleanly.

## Answer

In Kubernetes deployments, rolling updates terminate pods with `SIGTERM`. If a worker abruptly exits, in-flight agent runs are terminated mid-sentence, leaving orphaned state.

```python
import time
from typing import Optional


class GracefulAgentWorker:
    def __init__(self):
        self.stop_requested = False
        self.is_busy = False
        self.completed_jobs = 0

    def handle_shutdown_signal(self) -> None:
        self.stop_requested = True

    def process_job(self, job_id: str) -> str:
        self.is_busy = True
        try:
            # Simulate work
            time.sleep(0.01)
            self.completed_jobs += 1
            return f"Processed {job_id}"
        finally:
            self.is_busy = False

    def run_worker_cycle(self, queue: list) -> None:
        while not self.stop_requested and queue:
            job = queue.pop(0)
            self.process_job(job)


worker = GracefulAgentWorker()
mock_queue = ["job_1", "job_2", "job_3"]

# Run first job
worker.run_worker_cycle(mock_queue[:1])
assert worker.completed_jobs == 1

# Trigger shutdown signal
worker.handle_shutdown_signal()
assert worker.stop_requested is True

# Remaining queue items are not claimed
worker.run_worker_cycle(mock_queue[1:])
assert worker.completed_jobs == 1  # Unclaimed jobs stay in queue
```

## Likely follow-ups

- How does Kubernetes `terminationGracePeriodSeconds` interact with long-running agent tasks?
- What happens if an agent task requires 10 minutes to complete while Kubernetes enforces a 60-second grace period?

---

[← Q0816](../../batch_09_genai_services_fastapi/0816_dead_letter_queues_and_exponential_backoff_retry_policies/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0818 →](../../batch_09_genai_services_fastapi/0818_storing_conversation_history_in_nosql_dynamodb_and_cosmos_db/README.md)

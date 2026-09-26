# Q0878 · Worker memory leak mitigation: recycling worker processes after N tasks

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Easy |

## Question

Why do Python GenAI workers suffer from memory leaks over time, and write Python code demonstrating process recycle threshold logic.

## Answer

Python workers utilizing PyTorch, ONNX, tokenizers, or C-extensions often fail to release heap memory back to the operating system due to memory fragmentation or cyclic references.

Configuring Celery's `max_tasks_per_child` (e.g. 500 tasks) or Gunicorn's `max_requests` causes worker processes to exit gracefully after handling N tasks. The master supervisor spawns a fresh worker, reclaiming 100% of leaked RAM without downtime.

```python
class WorkerProcessSupervisor:
    def __init__(self, max_tasks_per_child: int = 3):
        self.max_tasks_per_child = max_tasks_per_child
        self.tasks_handled = 0
        self.worker_pid = 1001

    def handle_task(self, task_name: str) -> dict:
        self.tasks_handled += 1
        recycled = False

        if self.tasks_handled >= self.max_tasks_per_child:
            # Trigger process recycling
            self.worker_pid += 1  # Spawn fresh worker process
            self.tasks_handled = 0
            recycled = True

        return {
            "task": task_name,
            "handled_by_pid": self.worker_pid,
            "process_recycled": recycled,
        }


supervisor = WorkerProcessSupervisor(max_tasks_per_child=2)

t1 = supervisor.handle_task("embed_batch_1")
assert t1["handled_by_pid"] == 1001 and t1["process_recycled"] is False

t2 = supervisor.handle_task("embed_batch_2")
assert t2["handled_by_pid"] == 1002 and t2["process_recycled"] is True

t3 = supervisor.handle_task("embed_batch_3")
assert t3["handled_by_pid"] == 1002 and t3["process_recycled"] is False
```

## Likely follow-ups

- What is the difference between `max_tasks_per_child` and `max_memory_per_child`?
- How does Python's `gc.collect()` behave with C-extension allocations?

---

[← Q0877](../../batch_09_genai_services_fastapi/0877_distributed_task_workflows_chains_chords_and_groups_for/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0879 →](../../batch_09_genai_services_fastapi/0879_handling_unhandled_worker_exceptions_and_capturing_crash/README.md)

# Q0662 · A2A task cancellation and compensation

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Write Python code demonstrating A2A task cancellation with saga-style compensation for partial side effects.

## Answer

When a caller cancels a task via `DELETE /tasks/{id}` or `POST /tasks/{id}/cancel`, any non-idempotent side effects already committed (e.g. booked reservations or hold amounts) must be compensated.

```python
from typing import List


class CompensableAction:
    def __init__(self, name: str, undo_fn):
        self.name = name
        self.undo_fn = undo_fn


class A2ATaskExecutionWithSaga:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.status = "working"
        self._completed_actions: List[CompensableAction] = []

    def perform_action(self, action: CompensableAction) -> None:
        if self.status != "working":
            raise RuntimeError("Task not working")
        self._completed_actions.append(action)

    def cancel(self) -> List[str]:
        self.status = "cancelled"
        undo_log = []
        for action in reversed(self._completed_actions):
            action.undo_fn()
            undo_log.append(f"Compensated: {action.name}")
        self._completed_actions.clear()
        return undo_log


audit_log = []
task = A2ATaskExecutionWithSaga("tsk-trade-01")
task.perform_action(CompensableAction("Hold Collateral", lambda: audit_log.append("Released Collateral")))
task.perform_action(CompensableAction("Reserve Booking Slot", lambda: audit_log.append("Freed Booking Slot")))

compensations = task.cancel()
assert task.status == "cancelled"
assert len(compensations) == 2
assert audit_log == ["Freed Booking Slot", "Released Collateral"]
```

## Likely follow-ups

- What happens if a compensation action fails during cancellation?
- How does this saga pattern map to distributed database transactions?

---

[← Q0661](../../batch_07_mcp_a2a_skills_assistants/0661_a2a_push_notifications_and_webhook_delivery/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0663 →](../../batch_07_mcp_a2a_skills_assistants/0663_a2a_thread_and_context_propagation/README.md)

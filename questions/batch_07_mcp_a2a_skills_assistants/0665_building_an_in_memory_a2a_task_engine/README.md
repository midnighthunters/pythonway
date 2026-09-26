# Q0665 · Building an in-memory A2A task engine

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Hard |

## Question

Create an in-memory A2A Task Engine supporting task submission, execution simulation, status querying, and output part collection.

## Answer

```python
import uuid
from typing import Any, Dict, List, Optional


class InMemoryA2AEngine:
    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def submit_task(self, skill_id: str, input_parts: List[Dict[str, Any]]) -> str:
        task_id = f"tsk-{uuid.uuid4().hex[:8]}"
        self._tasks[task_id] = {
            "id": task_id,
            "skill_id": skill_id,
            "status": "submitted",
            "input": input_parts,
            "output": [],
        }
        return task_id

    def run_worker_step(self, task_id: str, result_text: str) -> None:
        task = self._tasks.get(task_id)
        if not task:
            raise KeyError("Task not found")
        task["status"] = "working"
        task["output"].append({"type": "text", "text": result_text})
        task["status"] = "completed"

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self._tasks.get(task_id)


engine = InMemoryA2AEngine()
tid = engine.submit_task("calculate_pnl", [{"type": "text", "text": "Trade TR-900"}])
assert engine.get_task(tid)["status"] == "submitted"

engine.run_worker_step(tid, "PnL is +$12,450.00")
res = engine.get_task(tid)
assert res["status"] == "completed"
assert res["output"][0]["text"] == "PnL is +$12,450.00"
```

## Likely follow-ups

- How would you persist this engine's state in PostgreSQL or DynamoDB?
- How do you handle distributed worker node crashes while in `working` status?

---

[← Q0664](../../batch_07_mcp_a2a_skills_assistants/0664_a2a_task_idempotency_with_client_tokens/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0666 →](../../batch_07_mcp_a2a_skills_assistants/0666_supervisor_worker_topology_using_a2a_protocol/README.md)

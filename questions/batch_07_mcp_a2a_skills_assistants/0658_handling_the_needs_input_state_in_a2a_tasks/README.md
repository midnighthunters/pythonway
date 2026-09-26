# Q0658 · Handling the needs_input state in A2A tasks

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Write Python code demonstrating how an A2A agent transitions a task into `needs_input`, specifies the required input prompt, and resumes execution once input is provided.

## Answer

Autonomous agents often need human approval (e.g. "Trade size exceeds $10M; confirm execution") or missing information (e.g. "Please provide account LEI code"). The agent updates the task status to `needs_input`.

```python
from typing import Any, Dict, Optional


class A2ATask:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.status = "working"
        self.prompt_for_input: Optional[str] = None
        self.provided_input: Optional[Dict[str, Any]] = None

    def request_input(self, prompt: str) -> None:
        self.status = "needs_input"
        self.prompt_for_input = prompt

    def submit_input(self, data: Dict[str, Any]) -> None:
        if self.status != "needs_input":
            raise RuntimeError(f"Cannot submit input: Task is in state '{self.status}'")
        self.provided_input = data
        self.prompt_for_input = None
        self.status = "working"


task = A2ATask("tsk-001")
task.request_input("Confirm transfer of $5,000,000 to account ACCT-9? (yes/no)")

assert task.status == "needs_input"
assert "Confirm transfer" in task.prompt_for_input

task.submit_input({"approved": True, "approver": "supervisor@jpmc.com"})
assert task.status == "working"
assert task.provided_input["approved"] is True
```

## Likely follow-ups

- What happens if the human supervisor does not respond within an SLA window?
- How does the calling agent subscribe to `needs_input` events over SSE?

---

[← Q0657](../../batch_07_mcp_a2a_skills_assistants/0657_a2a_parts_textpart_filepart_datapart/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0659 →](../../batch_07_mcp_a2a_skills_assistants/0659_a2a_server_sent_events_sse_streaming_of_task_progress/README.md)

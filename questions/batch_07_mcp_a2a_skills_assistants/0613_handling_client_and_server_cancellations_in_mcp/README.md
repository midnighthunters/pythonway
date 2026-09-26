# Q0613 · Handling client and server cancellations in MCP

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

Write Python code demonstrating how an MCP server processes `notifications/cancelled` to abort an in-flight long-running operation.

## Answer

When a user stops an agent in the UI, the client sends `notifications/cancelled` with `params: {"requestId": target_id, "reason": "User cancelled"}`. The server should check for cancellation flags or abort tokens.

```python
import threading
import time
from typing import Any, Dict, Set


class CancellableTaskRegistry:
    def __init__(self):
        self._cancelled_requests: Set[int] = set()

    def handle_cancelled_notification(self, params: Dict[str, Any]) -> None:
        req_id = params.get("requestId")
        if req_id is not None:
            self._cancelled_requests.add(req_id)

    def is_cancelled(self, req_id: int) -> bool:
        return req_id in self._cancelled_requests

    def run_simulated_task(self, req_id: int, total_steps: int) -> str:
        for step in range(total_steps):
            if self.is_cancelled(req_id):
                return f"Task {req_id} aborted at step {step}"
            time.sleep(0.01)
        return f"Task {req_id} completed successfully"


registry = CancellableTaskRegistry()
registry.handle_cancelled_notification({"requestId": 101, "reason": "User clicked stop"})
assert registry.is_cancelled(101) is True
assert registry.is_cancelled(102) is False

result = registry.run_simulated_task(101, 10)
assert "aborted" in result
```

## Likely follow-ups

- How does cancellation work across asynchronous boundaries in `asyncio`?
- If a server already completed a task before processing `notifications/cancelled`, what should it return?

---

[← Q0612](../../batch_07_mcp_a2a_skills_assistants/0612_notification_versus_request_in_mcp/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0614 →](../../batch_07_mcp_a2a_skills_assistants/0614_what_are_mcp_tools/README.md)

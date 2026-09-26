# Q0656 · A2A Task creation and submission

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Write Python code demonstrating the creation and submission of an A2A Task with input message parts and context metadata.

## Answer

When a client or orchestrator delegates work, it sends a `POST /tasks` request with a payload containing:
- `skill_id`: The skill being invoked.
- `input`: Array of message parts (text, structured data, files).
- `context`: Conversation and session identifiers.

```python
import uuid
from typing import Any, Dict, List


class A2ATaskClient:
    @staticmethod
    def create_task_payload(skill_id: str, prompt_text: str, structured_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        return {
            "task_id": str(uuid.uuid4()),
            "skill_id": skill_id,
            "status": "submitted",
            "context": {
                "session_id": session_id,
                "caller_id": "orchestrator-main",
            },
            "input": [
                {"type": "text", "text": prompt_text},
                {"type": "data", "data": structured_data},
            ],
        }


payload = A2ATaskClient.create_task_payload(
    skill_id="evaluate_counterparty_risk",
    prompt_text="Check credit default swap spread for Deutsche Bank.",
    structured_data={"cds_ticker": "DB_CDS_5Y", "threshold_bps": 120},
    session_id="sess-8899",
)

assert payload["status"] == "submitted"
assert payload["skill_id"] == "evaluate_counterparty_risk"
assert len(payload["input"]) == 2
assert payload["input"][0]["type"] == "text"
assert payload["input"][1]["data"]["threshold_bps"] == 120
```

## Likely follow-ups

- How does an A2A server acknowledge task creation?
- What HTTP status code should `POST /tasks` return (201 Created vs 202 Accepted)?

---

[← Q0655](../../batch_07_mcp_a2a_skills_assistants/0655_a2a_task_state_machine_and_lifecycle/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0657 →](../../batch_07_mcp_a2a_skills_assistants/0657_a2a_parts_textpart_filepart_datapart/README.md)

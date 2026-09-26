# Q0660 · Parsing A2A streaming event frames in Python

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Write a Python parser for A2A SSE streams that processes raw chunked text and yields parsed event objects.

## Answer

```python
import json
from typing import Any, Dict, Generator, Optional


class A2ASSEParser:
    @staticmethod
    def parse_stream(raw_text: str) -> Generator[Dict[str, Any], None, None]:
        current_event: Optional[str] = None
        current_data: list = []

        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                if current_event and current_data:
                    payload = "\n".join(current_data)
                    yield {"event": current_event, "data": json.loads(payload)}
                current_event = None
                current_data = []
                continue

            if line.startswith("event:"):
                current_event = line[len("event:"):].strip()
            elif line.startswith("data:"):
                current_data.append(line[len("data:"):].strip())

        if current_event and current_data:
            yield {"event": current_event, "data": json.loads("\n".join(current_data))}


mock_sse = (
    'event: status_change\n'
    'data: {"status": "working"}\n\n'
    'event: part_stream\n'
    'data: {"delta": "Fetching records"}\n\n'
)

events = list(A2ASSEParser.parse_stream(mock_sse))
assert len(events) == 2
assert events[0]["event"] == "status_change"
assert events[0]["data"]["status"] == "working"
assert events[1]["event"] == "part_stream"
assert events[1]["data"]["delta"] == "Fetching records"
```

## Likely follow-ups

- How does the parser handle multi-line `data:` entries?
- How should malformed JSON in SSE payloads be handled?

---

[← Q0659](../../batch_07_mcp_a2a_skills_assistants/0659_a2a_server_sent_events_sse_streaming_of_task_progress/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0661 →](../../batch_07_mcp_a2a_skills_assistants/0661_a2a_push_notifications_and_webhook_delivery/README.md)

# Q0611 · Parsing stdio stream into JSON-RPC messages

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

Write a Python generator that processes a buffered text stream (simulating `sys.stdin`), splits lines, and yields complete JSON-RPC message dictionaries while ignoring whitespace and blank lines.

## Answer

In stdio transport, messages are serialized as single-line JSON strings terminated by `\n`. Any internal newlines inside strings must be escaped (`\n`).

```python
import io
import json
from typing import Generator, Dict, Any


def parse_stdio_stream(stream: io.StringIO) -> Generator[Dict[str, Any], None, None]:
    for line in stream:
        clean = line.strip()
        if not clean:
            continue
        try:
            msg = json.loads(clean)
            if isinstance(msg, dict) and msg.get("jsonrpc") == "2.0":
                yield msg
        except json.JSONDecodeError:
            continue


buffer = io.StringIO(
    '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}\n\n   \n{"jsonrpc": "2.0", "method": "notifications/initialized"}\ninvalid-non-json-line\n{"jsonrpc": "2.0", "id": 2, "result": {"status": "ok"}}\n'
)

messages = list(parse_stdio_stream(buffer))
assert len(messages) == 3
assert messages[0]["id"] == 1
assert messages[1]["method"] == "notifications/initialized"
assert messages[2]["result"]["status"] == "ok"
```

## Likely follow-ups

- Why must an MCP server on stdio never flush carriage returns or raw log strings to stdout?
- What buffer size considerations apply when handling multi-megabyte tool payloads over stdio?

---

[← Q0610](../../batch_07_mcp_a2a_skills_assistants/0610_building_a_minimal_json_rpc_2_0_message_parser_and_builder/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0612 →](../../batch_07_mcp_a2a_skills_assistants/0612_notification_versus_request_in_mcp/README.md)

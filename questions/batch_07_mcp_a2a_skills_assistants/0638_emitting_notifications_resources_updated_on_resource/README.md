# Q0638 · Emitting notifications/resources/updated on resource mutation

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

Write Python code demonstrating how an MCP server emits a `notifications/resources/updated` notification when an underlying resource is modified.

## Answer

When data behind a subscribed URI changes (e.g. a file is saved, a database record updates), the server sends `notifications/resources/updated` with `params: {"uri": "..."}` to subscribed clients.

```python
from typing import Any, Dict, List


class MCPResourcePublisher:
    def __init__(self):
        self.emitted_notifications: List[Dict[str, Any]] = []

    def notify_resource_updated(self, uri: str) -> None:
        msg = {
            "jsonrpc": "2.0",
            "method": "notifications/resources/updated",
            "params": {"uri": uri},
        }
        self.emitted_notifications.append(msg)


publisher = MCPResourcePublisher()
publisher.notify_resource_updated("rates://fx/spot/GBPUSD")

assert len(publisher.emitted_notifications) == 1
assert publisher.emitted_notifications[0]["method"] == "notifications/resources/updated"
assert publisher.emitted_notifications[0]["params"]["uri"] == "rates://fx/spot/GBPUSD"
assert "id" not in publisher.emitted_notifications[0]
```

## Likely follow-ups

- Should the notification include the new data content or just the URI?
- How can rapid successive updates be debounced to prevent flooding clients?

---

[← Q0637](../../batch_07_mcp_a2a_skills_assistants/0637_subscribing_to_resource_updates_with_resources_subscribe/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0639 →](../../batch_07_mcp_a2a_skills_assistants/0639_implementing_an_in_memory_resource_store_with_mime_types/README.md)

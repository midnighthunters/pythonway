# Q0637 · Subscribing to resource updates with resources/subscribe

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

Write Python code implementing the MCP `resources/subscribe` and `resources/unsubscribe` methods for a stateful server.

## Answer

When a server advertises `resources: {"subscribe": true}`, clients can subscribe to specific resource URIs. When that resource changes, the server notifies subscribers so they can refresh stale context.

```python
from typing import Any, Dict, Set


class MCPResourceSubscriptionManager:
    def __init__(self):
        self._subscribers: Dict[str, Set[str]] = {}

    def handle_subscribe(self, client_id: str, uri: str) -> Dict[str, Any]:
        if uri not in self._subscribers:
            self._subscribers[uri] = set()
        self._subscribers[uri].add(client_id)
        return {"result": {}}

    def handle_unsubscribe(self, client_id: str, uri: str) -> Dict[str, Any]:
        if uri in self._subscribers and client_id in self._subscribers[uri]:
            self._subscribers[uri].remove(client_id)
        return {"result": {}}

    def get_subscribers_for_uri(self, uri: str) -> Set[str]:
        return self._subscribers.get(uri, set())


manager = MCPResourceSubscriptionManager()
manager.handle_subscribe("client-1", "rates://fx/spot")
manager.handle_subscribe("client-2", "rates://fx/spot")
manager.handle_subscribe("client-1", "rates://rates/libor")

assert len(manager.get_subscribers_for_uri("rates://fx/spot")) == 2

manager.handle_unsubscribe("client-1", "rates://fx/spot")
assert manager.get_subscribers_for_uri("rates://fx/spot") == {"client-2"}
```

## Likely follow-ups

- What notification message is sent to subscribers when a resource updates?
- How should subscriptions be cleaned up when a client disconnects unexpectedly?

---

[← Q0636](../../batch_07_mcp_a2a_skills_assistants/0636_resource_templates_with_rfc_6570_uri_templates/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0638 →](../../batch_07_mcp_a2a_skills_assistants/0638_emitting_notifications_resources_updated_on_resource/README.md)

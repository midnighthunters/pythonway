# Q0639 · Implementing an in-memory resource store with MIME types

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

Build a complete in-memory MCP Resource Registry supporting registration, listing, reading, and MIME type introspection.

## Answer

```python
from typing import Any, Dict, List, Optional


class FullResourceRegistry:
    def __init__(self):
        self._resources: Dict[str, Dict[str, Any]] = {}

    def register(self, uri: str, name: str, mime_type: str, content: str, description: str = "") -> None:
        self._resources[uri] = {
            "uri": uri,
            "name": name,
            "mimeType": mime_type,
            "description": description,
            "content": content,
        }

    def list_resources(self) -> List[Dict[str, Any]]:
        return [
            {"uri": r["uri"], "name": r["name"], "mimeType": r["mimeType"], "description": r["description"]}
            for r in self._resources.values()
        ]

    def read_resource(self, uri: str) -> Optional[Dict[str, Any]]:
        r = self._resources.get(uri)
        if not r:
            return None
        return {
            "contents": [
                {
                    "uri": r["uri"],
                    "mimeType": r["mimeType"],
                    "text": r["content"],
                }
            ]
        }


reg = FullResourceRegistry()
reg.register("config://app/env", "App Config", "application/json", '{"env": "production", "region": "ldn"}')

catalog = reg.list_resources()
assert len(catalog) == 1
assert catalog[0]["name"] == "App Config"

data = reg.read_resource("config://app/env")
assert data is not None
assert '"production"' in data["contents"][0]["text"]
```

## Likely follow-ups

- How does the host determine if an LLM can understand the declared MIME type?
- How would you handle large files that exceed RAM by reading from disk on demand?

---

[← Q0638](../../batch_07_mcp_a2a_skills_assistants/0638_emitting_notifications_resources_updated_on_resource/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0640 →](../../batch_07_mcp_a2a_skills_assistants/0640_access_control_on_sensitive_resources_by_uri_pattern/README.md)

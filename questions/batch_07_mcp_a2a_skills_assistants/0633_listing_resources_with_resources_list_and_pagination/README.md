# Q0633 · Listing resources with resources/list and pagination

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

Write Python code implementing the MCP `resources/list` method with cursor pagination and metadata fields.

## Answer

Clients discover available resources by issuing `resources/list`. Each resource definition must include `uri`, `name`, and optional fields `description`, `mimeType`, and `size`.

```python
from typing import Any, Dict, List, Optional


class MCPResourceCatalog:
    def __init__(self, page_size: int = 2):
        self.page_size = page_size
        self._resources: List[Dict[str, Any]] = []

    def add_resource(self, uri: str, name: str, mime_type: str, desc: str = "") -> None:
        self._resources.append({
            "uri": uri,
            "name": name,
            "description": desc,
            "mimeType": mime_type,
        })

    def handle_list(self, cursor: Optional[str] = None) -> Dict[str, Any]:
        start = int(cursor) if cursor and cursor.isdigit() else 0
        end = start + self.page_size
        items = self._resources[start:end]

        res: Dict[str, Any] = {"resources": items}
        if end < len(self._resources):
            res["nextCursor"] = str(end)
        return res


catalog = MCPResourceCatalog(page_size=2)
catalog.add_resource("policy://kyc/v1", "KYC Policy", "text/markdown")
catalog.add_resource("policy://aml/v2", "AML Guidelines", "text/markdown")
catalog.add_resource("schema://db/trades", "Trades DDL", "application/sql")

p1 = catalog.handle_list()
assert len(p1["resources"]) == 2
assert p1["resources"][0]["uri"] == "policy://kyc/v1"
assert p1["nextCursor"] == "2"

p2 = catalog.handle_list(cursor=p1["nextCursor"])
assert len(p2["resources"]) == 1
assert p2["resources"][0]["uri"] == "schema://db/trades"
assert "nextCursor" not in p2
```

## Likely follow-ups

- How does the client present available resources to the user in a chat interface?
- When should a server expose dynamic resource templates instead of a static resource list?

---

[← Q0632](../../batch_07_mcp_a2a_skills_assistants/0632_mcp_resource_uri_schemes_and_structure/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0634 →](../../batch_07_mcp_a2a_skills_assistants/0634_reading_resource_content_with_resources_read/README.md)

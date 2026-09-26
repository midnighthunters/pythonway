# Q0636 · Resource templates with RFC 6570 URI templates

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

Explain RFC 6570 URI templates in MCP. Write Python code that matches an incoming URI against a resource template and extracts parameter variables.

## Answer

Static `resources/list` cannot enumerate millions of database records or account files. MCP supports Resource Templates:
- Servers advertise patterns via `resources/templates/list` with RFC 6570 URI templates (e.g. `trades://accounts/{account_id}/history/{year}`).
- Clients match dynamic URIs against templates to discover which server can satisfy the read.

```python
import re
from typing import Any, Dict, Optional


class MCPResourceTemplate:
    def __init__(self, name: str, uri_template: str, mime_type: str):
        self.name = name
        self.uri_template = uri_template
        self.mime_type = mime_type
        # Extract placeholders like {account_id}
        keys = re.findall(r"\{([a-zA-Z0-9_]+)\}", uri_template)
        pattern = uri_template
        for k in keys:
            pattern = pattern.replace(f"{{{k}}}", f"(?P<{k}>[^/]+)")
        self._regex = re.compile(f"^{pattern}$")

    def match(self, uri: str) -> Optional[Dict[str, str]]:
        match = self._regex.match(uri)
        return match.groupdict() if match else None


tmpl = MCPResourceTemplate("account_trades", "trades://accounts/{account_id}/records/{year}", "application/json")
params = tmpl.match("trades://accounts/ACC-101/records/2026")
assert params == {"account_id": "ACC-101", "year": "2026"}

no_match = tmpl.match("trades://unknown/path")
assert no_match is None
```

## Likely follow-ups

- How does the client notify users of available resource templates?
- Can resource templates include optional query parameters (`{?limit,offset}`)?

---

[← Q0635](../../batch_07_mcp_a2a_skills_assistants/0635_implementing_text_versus_binary_resources/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0637 →](../../batch_07_mcp_a2a_skills_assistants/0637_subscribing_to_resource_updates_with_resources_subscribe/README.md)

# Q0634 · Reading resource content with resources/read

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

Write Python code for an MCP server handling `resources/read`, returning text contents or error codes for missing URIs.

## Answer

When a client requests `resources/read` with `params: {"uri": "..."}`, the server locates the resource and returns an array of content objects:
```json
{
  "contents": [
    {
      "uri": "policy://kyc/v1",
      "mimeType": "text/markdown",
      "text": "# KYC Policy Content..."
    }
  ]
}
```

```python
from typing import Any, Dict


class MCPResourceServer:
    def __init__(self):
        self._store: Dict[str, Dict[str, str]] = {}

    def set_resource(self, uri: str, mime_type: str, text: str) -> None:
        self._store[uri] = {"mimeType": mime_type, "text": text}

    def handle_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        uri = params.get("uri")
        if not uri or uri not in self._store:
            return {
                "error": {
                    "code": -32002,
                    "message": f"Resource not found: '{uri}'",
                }
            }

        item = self._store[uri]
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": item["mimeType"],
                    "text": item["text"],
                }
            ]
        }


server = MCPResourceServer()
server.set_resource("docs://rules/risk", "text/plain", "Maximum intraday leverage is 5x.")

res = server.handle_read({"uri": "docs://rules/risk"})
assert "contents" in res
assert res["contents"][0]["text"] == "Maximum intraday leverage is 5x."

err = server.handle_read({"uri": "docs://nonexistent"})
assert "error" in err
assert err["error"]["code"] == -32002
```

## Likely follow-ups

- Can `resources/read` return multiple content items for a single URI request?
- How should a server handle reads on resources that require dynamic calculation?

---

[← Q0633](../../batch_07_mcp_a2a_skills_assistants/0633_listing_resources_with_resources_list_and_pagination/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0635 →](../../batch_07_mcp_a2a_skills_assistants/0635_implementing_text_versus_binary_resources/README.md)

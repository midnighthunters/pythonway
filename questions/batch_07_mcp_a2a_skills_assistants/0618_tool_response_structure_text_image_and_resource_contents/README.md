# Q0618 · Tool response structure: text, image and resource contents

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Show how an MCP tool response can combine text, base64-encoded images, and embedded resource links in a single `tools/call` response.

## Answer

An MCP tool result `content` array can contain multiple items of varying MIME types:
- `text`: Plain text or JSON strings.
- `image`: Binary images encoded as base64 with a declared `mimeType` (e.g. `"image/png"`).
- `resource`: An embedded resource object referencing a URI and providing text or blob contents.

```python
import base64
from typing import Any, Dict, List


def make_multimodal_tool_result(summary: str, raw_png_bytes: bytes, report_uri: str) -> Dict[str, Any]:
    b64_image = base64.b64encode(raw_png_bytes).decode("ascii")

    content: List[Dict[str, Any]] = [
        {"type": "text", "text": summary},
        {"type": "image", "data": b64_image, "mimeType": "image/png"},
        {
            "type": "resource",
            "resource": {
                "uri": report_uri,
                "mimeType": "application/json",
                "text": '{"compliance_checked": true, "signoff": "approved"}',
            },
        },
    ]

    return {"content": content, "isError": False}


mock_png = b"\x89PNG\r\n\x1a\n\x00fake_image_bytes"
result = make_multimodal_tool_result("Risk analysis chart generated.", mock_png, "reports://risk/q3-summary")

assert len(result["content"]) == 3
assert result["content"][0]["type"] == "text"
assert result["content"][1]["type"] == "image"
assert result["content"][1]["mimeType"] == "image/png"
assert result["content"][2]["resource"]["uri"] == "reports://risk/q3-summary"
```

## Likely follow-ups

- Which LLM models can natively ingest the `image` content block from an MCP tool?
- When should a tool return an embedded resource versus returning a URI for the client to fetch separately?

---

[← Q0617](../../batch_07_mcp_a2a_skills_assistants/0617_handling_tools_call_requests/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0619 →](../../batch_07_mcp_a2a_skills_assistants/0619_reporting_tool_errors_iserror_flag_versus_json_rpc_error/README.md)

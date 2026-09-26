# Q0635 · Implementing text versus binary resources

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

How does MCP handle binary resources (e.g. PDFs, images, Parquet files)? Write Python code that formats a binary image resource using base64 encoding.

## Answer

In MCP, resource content objects must include either:
- `text`: A string containing UTF-8 text (for JSON, Markdown, source code, text files).
- `blob`: A base64-encoded string representing binary bytes (for PDFs, PNG images, binary data), along with the `mimeType`.

```python
import base64
from typing import Any, Dict


def package_binary_resource(uri: str, mime_type: str, raw_bytes: bytes) -> Dict[str, Any]:
    encoded_blob = base64.b64encode(raw_bytes).decode("ascii")
    return {
        "contents": [
            {
                "uri": uri,
                "mimeType": mime_type,
                "blob": encoded_blob,
            }
        ]
    }


pdf_header = b"%PDF-1.7 mock binary content..."
res = package_binary_resource("reports://2026/annual_audit.pdf", "application/pdf", pdf_header)

assert res["contents"][0]["uri"] == "reports://2026/annual_audit.pdf"
assert res["contents"][0]["mimeType"] == "application/pdf"
assert "blob" in res["contents"][0]
assert base64.b64decode(res["contents"][0]["blob"]) == pdf_header
```

## Likely follow-ups

- What is the memory impact of base64 encoding on large 100MB documents?
- How can an MCP server stream large binary resources chunk by chunk?

---

[← Q0634](../../batch_07_mcp_a2a_skills_assistants/0634_reading_resource_content_with_resources_read/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0636 →](../../batch_07_mcp_a2a_skills_assistants/0636_resource_templates_with_rfc_6570_uri_templates/README.md)

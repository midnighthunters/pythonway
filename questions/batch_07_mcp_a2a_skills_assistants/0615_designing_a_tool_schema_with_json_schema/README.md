# Q0615 · Designing a tool schema with JSON Schema

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Construct an MCP tool definition for an enterprise trade break inquiry tool using valid JSON Schema, specifying parameter types, descriptions, and required fields.

## Answer

In MCP, the `inputSchema` property must be a valid JSON Schema object (typically Draft 7 or Draft 2020-12) describing the parameters accepted by `tools/call`.

```python
TRADE_BREAK_TOOL = {
    "name": "query_trade_breaks",
    "description": "Searches for trade settlement breaks by account ID, date range, and break status.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "account_id": {
                "type": "string",
                "pattern": "^[A-Z]{3}-[0-9]{6}$",
                "description": "The enterprise account identifier, e.g. 'LDN-123456'.",
            },
            "status": {
                "type": "string",
                "enum": ["OPEN", "PENDING_INVESTIGATION", "RESOLVED"],
                "default": "OPEN",
                "description": "Current status of the settlement break.",
            },
            "min_amount": {
                "type": "number",
                "minimum": 0.0,
                "description": "Optional minimum discrepancy amount in USD.",
            },
        },
        "required": ["account_id"],
        "additionalProperties": False,
    },
}

assert TRADE_BREAK_TOOL["name"] == "query_trade_breaks"
assert TRADE_BREAK_TOOL["inputSchema"]["required"] == ["account_id"]
assert TRADE_BREAK_TOOL["inputSchema"]["additionalProperties"] is False
```

## Likely follow-ups

- Why is setting `additionalProperties: False` recommended for LLM tool schemas?
- How do regex patterns inside JSON Schema help prevent prompt injection and malformed inputs?

---

[← Q0614](../../batch_07_mcp_a2a_skills_assistants/0614_what_are_mcp_tools/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0616 →](../../batch_07_mcp_a2a_skills_assistants/0616_listing_tools_with_tools_list_and_pagination/README.md)

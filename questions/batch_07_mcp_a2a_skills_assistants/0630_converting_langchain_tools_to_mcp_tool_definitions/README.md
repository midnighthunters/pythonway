# Q0630 · Converting LangChain tools to MCP tool definitions

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Write Python code that inspects a LangChain `@tool` decorated function and generates a valid MCP `tools/list` entry with JSON Schema.

## Answer

```python
from typing import Any, Dict
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class FXQueryInput(BaseModel):
    base: str = Field(description="Base currency ISO code", min_length=3, max_length=3)
    quote: str = Field(description="Quote currency ISO code", min_length=3, max_length=3)


@tool(args_schema=FXQueryInput)
def fetch_fx_quote(base: str, quote: str) -> str:
    '''Fetches the real-time spot FX quote between base and quote currencies.'''
    return f"Quote {base}/{quote}: 1.2500"


def langchain_tool_to_mcp(lc_tool) -> Dict[str, Any]:
    schema = lc_tool.args_schema.model_json_schema() if lc_tool.args_schema else {"type": "object", "properties": {}}
    schema.pop("title", None)
    return {
        "name": lc_tool.name,
        "description": lc_tool.description or "",
        "inputSchema": schema,
    }


mcp_def = langchain_tool_to_mcp(fetch_fx_quote)
assert mcp_def["name"] == "fetch_fx_quote"
assert "real-time spot FX" in mcp_def["description"]
assert "base" in mcp_def["inputSchema"]["properties"]
assert "quote" in mcp_def["inputSchema"]["required"]
```

## Likely follow-ups

- How does LangChain 1.x support connecting directly to an MCP server as a tool provider?
- What schema discrepancies can occur when converting nested Pydantic models to JSON Schema?

---

[← Q0629](../../batch_07_mcp_a2a_skills_assistants/0629_caching_idempotent_mcp_tool_call_responses/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0631 →](../../batch_07_mcp_a2a_skills_assistants/0631_what_are_mcp_resources_and_how_do_they_differ_from_tools/README.md)

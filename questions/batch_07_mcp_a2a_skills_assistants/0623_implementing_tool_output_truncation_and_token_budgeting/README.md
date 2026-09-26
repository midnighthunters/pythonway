# Q0623 · Implementing tool output truncation and token budgeting

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

An MCP server query returns a 50,000-row database result that would blow past the LLM's context window. Implement a tool output trimmer that enforces character limits and appends a truncation warning.

## Answer

Large tool outputs cause context overflow, high inference cost, and latency spikes. An enterprise MCP tool must enforce max character/token budgets:

```python
from typing import Any, Dict


def format_bounded_tool_output(raw_output: str, max_chars: int = 1000) -> Dict[str, Any]:
    if len(raw_output) <= max_chars:
        return {"content": [{"type": "text", "text": raw_output}], "isError": False}

    truncated = raw_output[:max_chars]
    omitted = len(raw_output) - max_chars
    warning = "\n\n[WARNING: Output truncated. " + str(omitted) + " characters omitted. Refine query filters.]"

    return {
        "content": [{"type": "text", "text": truncated + warning}],
        "isError": False,
    }


short_text = "Transaction TX-100: Approved."
res_short = format_bounded_tool_output(short_text, max_chars=100)
assert res_short["content"][0]["text"] == short_text

huge_text = "Row data: " + ("A" * 5000)
res_huge = format_bounded_tool_output(huge_text, max_chars=500)
assert len(res_huge["content"][0]["text"]) > 500
assert "WARNING: Output truncated" in res_huge["content"][0]["text"]
```

## Likely follow-ups

- Should truncation happen at the MCP server or at the MCP client?
- How can a tool provide a URI resource link so the agent can read chunks on demand?

---

[← Q0622](../../batch_07_mcp_a2a_skills_assistants/0622_building_an_in_memory_mcp_tool_registry_and_dispatcher/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0624 →](../../batch_07_mcp_a2a_skills_assistants/0624_dynamic_tool_registration_and_tools_list_changed/README.md)

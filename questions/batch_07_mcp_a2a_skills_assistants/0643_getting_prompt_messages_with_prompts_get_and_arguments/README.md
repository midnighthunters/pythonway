# Q0643 · Getting prompt messages with prompts/get and arguments

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Medium |

## Question

Write Python code handling `prompts/get`, substituting arguments into a parameterized prompt template and returning structured messages.

## Answer

When a user or client selects a prompt, the client sends `prompts/get` with `params: {"name": "...", "arguments": {"arg1": "val1"}}`. The server evaluates the template and returns structured messages.

```python
from typing import Any, Dict, List


def handle_prompts_get(prompt_name: str, arguments: Dict[str, str]) -> Dict[str, Any]:
    if prompt_name == "audit_trade":
        trade_id = arguments.get("trade_id", "UNKNOWN")
        messages = [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"Please conduct a comprehensive regulatory audit for trade {trade_id}. Check settlement dates and counterparty limits.",
                },
            }
        ]
        return {
            "description": f"Audit review for {trade_id}",
            "messages": messages,
        }

    return {"error": {"code": -32602, "message": f"Unknown prompt: {prompt_name}"}}


res = handle_prompts_get("audit_trade", {"trade_id": "TRD-9988"})
assert "messages" in res
assert "TRD-9988" in res["messages"][0]["content"]["text"]
```

## Likely follow-ups

- Can `prompts/get` return an assistant role message as well as a user role message?
- How should missing required arguments be reported in `prompts/get`?

---

[← Q0642](../../batch_07_mcp_a2a_skills_assistants/0642_listing_prompt_templates_with_prompts_list/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0644 →](../../batch_07_mcp_a2a_skills_assistants/0644_mapping_prompt_messages_to_llm_roles/README.md)

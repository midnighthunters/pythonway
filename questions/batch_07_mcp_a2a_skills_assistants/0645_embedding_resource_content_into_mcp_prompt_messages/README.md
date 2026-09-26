# Q0645 · Embedding resource content into MCP prompt messages

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Medium |

## Question

Write Python code demonstrating how an MCP server embeds an internal Resource directly into a Prompt response using `resource` content blocks.

## Answer

Rather than requiring the client to issue a separate `resources/read` call, an MCP prompt can directly embed resource content into the prompt messages.

```python
from typing import Any, Dict


def make_prompt_with_embedded_resource(rule_id: str, rule_text: str) -> Dict[str, Any]:
    return {
        "description": "Compliance review prompt with attached rulebook",
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "resource",
                    "resource": {
                        "uri": f"rules://internal/{rule_id}",
                        "mimeType": "text/markdown",
                        "text": rule_text,
                    },
                },
            },
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "Based on the rulebook above, review whether this trade adheres to compliance guidelines.",
                },
            },
        ],
    }


res = make_prompt_with_embedded_resource("SEC-15C3", "Net Capital Rule: Broker-dealers must maintain net liquid assets.")
assert len(res["messages"]) == 2
assert res["messages"][0]["content"]["type"] == "resource"
assert res["messages"][0]["content"]["resource"]["uri"] == "rules://internal/SEC-15C3"
```

## Likely follow-ups

- What are the advantages of embedding resources directly into prompt templates?
- How should the client format an embedded resource block when transmitting to an LLM provider?

---

[← Q0644](../../batch_07_mcp_a2a_skills_assistants/0644_mapping_prompt_messages_to_llm_roles/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0646 →](../../batch_07_mcp_a2a_skills_assistants/0646_dynamic_prompt_template_evaluation_with_parameter_validation/README.md)

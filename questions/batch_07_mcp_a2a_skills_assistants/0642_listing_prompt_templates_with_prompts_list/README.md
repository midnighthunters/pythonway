# Q0642 · Listing prompt templates with prompts/list

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Medium |

## Question

Write Python code for an MCP server that implements `prompts/list`, returning prompt names, descriptions, and argument schemas.

## Answer

Clients query `prompts/list` to show available workflows in dropdowns or slash-command menus (e.g. `/investigate-break`).

```python
from typing import Any, Dict, List


class MCPPromptCatalog:
    def __init__(self):
        self._prompts: Dict[str, Dict[str, Any]] = {}

    def register_prompt(self, name: str, description: str, arguments: List[Dict[str, Any]]) -> None:
        self._prompts[name] = {
            "name": name,
            "description": description,
            "arguments": arguments,
        }

    def handle_list(self) -> Dict[str, Any]:
        return {"prompts": list(self._prompts.values())}


catalog = MCPPromptCatalog()
catalog.register_prompt(
    name="review_trade_break",
    description="Analyzes an unhedged FX trade break and recommends resolution actions.",
    arguments=[
        {"name": "break_id", "description": "Trade break identifier, e.g. BRK-100", "required": True},
        {"name": "urgency", "description": "Low, medium, or high urgency", "required": False},
    ],
)

res = catalog.handle_list()
assert len(res["prompts"]) == 1
assert res["prompts"][0]["name"] == "review_trade_break"
assert res["prompts"][0]["arguments"][0]["name"] == "break_id"
```

## Likely follow-ups

- How do slash-commands in AI chat interfaces map to MCP prompts?
- What happens if a client passes an argument not declared in the prompt schema?

---

[← Q0641](../../batch_07_mcp_a2a_skills_assistants/0641_what_are_mcp_prompts_and_use_cases/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0643 →](../../batch_07_mcp_a2a_skills_assistants/0643_getting_prompt_messages_with_prompts_get_and_arguments/README.md)

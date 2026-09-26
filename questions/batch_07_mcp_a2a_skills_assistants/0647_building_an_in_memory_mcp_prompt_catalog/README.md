# Q0647 · Building an in-memory MCP prompt catalog

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Medium |

## Question

Write Python code for an in-memory MCP prompt registry supporting registration, schema listing, and invocation.

## Answer

```python
from typing import Any, Callable, Dict, List, Optional


class MCPPromptRegistry:
    def __init__(self):
        self._prompts: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Callable[[Dict[str, str]], List[Dict[str, Any]]]] = {}

    def register(self, name: str, description: str, args: List[Dict[str, Any]], handler: Callable[[Dict[str, str]], List[Dict[str, Any]]]):
        self._prompts[name] = {"name": name, "description": description, "arguments": args}
        self._handlers[name] = handler

    def list_prompts(self) -> List[Dict[str, Any]]:
        return list(self._prompts.values())

    def get_prompt(self, name: str, arguments: Dict[str, str]) -> Optional[Dict[str, Any]]:
        if name not in self._prompts:
            return None
        messages = self._handlers[name](arguments)
        return {"description": self._prompts[name]["description"], "messages": messages}


reg = MCPPromptRegistry()
reg.register(
    "explain_var",
    "Explains Value at Risk calculation",
    [{"name": "confidence", "required": True}],
    lambda args: [{"role": "user", "content": {"type": "text", "text": f"Explain VaR at {args.get('confidence')}%."}}],
)

assert len(reg.list_prompts()) == 1
res = reg.get_prompt("explain_var", {"confidence": "99"})
assert res is not None
assert "99%" in res["messages"][0]["content"]["text"]
```

## Likely follow-ups

- How does the registry manage prompt versioning?
- What notification informs clients when a prompt is added or updated?

---

[← Q0646](../../batch_07_mcp_a2a_skills_assistants/0646_dynamic_prompt_template_evaluation_with_parameter_validation/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0648 →](../../batch_07_mcp_a2a_skills_assistants/0648_notifying_clients_with_notifications_prompts_list_changed/README.md)

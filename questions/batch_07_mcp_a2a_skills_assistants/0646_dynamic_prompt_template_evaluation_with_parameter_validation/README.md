# Q0646 · Dynamic prompt template evaluation with parameter validation

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Medium |

## Question

Implement a parameter-validated prompt evaluation engine that replaces template placeholders (e.g. `{{account_id}}`) and validates types.

## Answer

```python
import re
from typing import Any, Dict


class SafePromptEngine:
    @staticmethod
    def render(template: str, variables: Dict[str, str], required_vars: set) -> str:
        for var in required_vars:
            if var not in variables or not variables[var].strip():
                raise ValueError(f"Missing required prompt variable: '{var}'")

        def _replace(match):
            key = match.group(1).strip()
            return str(variables.get(key, ""))

        return re.sub(r"\{\{([a-zA-Z0-9_]+)\}\}", _replace, template)


tmpl = "Analyze risk for account {{account_id}} in jurisdiction {{region}}."
rendered = SafePromptEngine.render(tmpl, {"account_id": "LDN-101", "region": "EMEA"}, required_vars={"account_id", "region"})
assert rendered == "Analyze risk for account LDN-101 in jurisdiction EMEA."

try:
    SafePromptEngine.render(tmpl, {"account_id": "LDN-101"}, required_vars={"account_id", "region"})
    assert False, "Should raise ValueError"
except ValueError as exc:
    assert "region" in str(exc)
```

## Likely follow-ups

- Why should raw user input in prompt templates be sanitized before rendering?
- How can Jinja2 templates be safely sandboxed against arbitrary code execution?

---

[← Q0645](../../batch_07_mcp_a2a_skills_assistants/0645_embedding_resource_content_into_mcp_prompt_messages/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0647 →](../../batch_07_mcp_a2a_skills_assistants/0647_building_an_in_memory_mcp_prompt_catalog/README.md)

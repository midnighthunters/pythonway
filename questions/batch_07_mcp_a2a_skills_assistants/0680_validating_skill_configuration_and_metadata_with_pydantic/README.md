# Q0680 · Validating skill configuration and metadata with Pydantic

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

Write Python code using Pydantic to validate a `SKILL.md` YAML frontmatter configuration block.

## Answer

```python
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError


class SkillMetadata(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    description: str = Field(min_length=10)
    tags: List[str] = Field(default_factory=list)
    requires_approval: bool = False
    timeout_seconds: int = Field(default=30, ge=1, le=300)


valid_data = {
    "name": "credit_risk_analyzer",
    "version": "1.2.0",
    "description": "Calculates credit default probabilities for corporate counterparties.",
    "tags": ["risk", "credit", "corporate"],
    "requires_approval": True,
    "timeout_seconds": 60,
}

meta = SkillMetadata.model_validate(valid_data)
assert meta.name == "credit_risk_analyzer"
assert meta.requires_approval is True

try:
    SkillMetadata.model_validate({"name": "bad", "version": "v1", "description": "short"})
    assert False, "Should raise ValidationError"
except ValidationError:
    pass
```

## Likely follow-ups

- Why should skill metadata include a `requires_approval` flag?
- How do tags assist in skill discovery and role-based entitlement filtering?

---

[← Q0679](../../batch_07_mcp_a2a_skills_assistants/0679_loading_skills_on_demand_based_on_user_intent/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0681 →](../../batch_07_mcp_a2a_skills_assistants/0681_sandboxing_skill_execution_in_isolated_runtimes/README.md)

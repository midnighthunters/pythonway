# Q0654 · Validating an A2A Agent Card against JSON schema

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Write Python code using Pydantic to validate an incoming A2A Agent Card, verifying required fields, URLs, and skill definitions.

## Answer

```python
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError


class SkillDefinition(BaseModel):
    id: str
    name: str
    inputSchema: Dict[str, Any] = Field(default_factory=dict)
    outputSchema: Optional[Dict[str, Any]] = None


class AgentCapabilities(BaseModel):
    streaming: bool = False
    push_notifications: bool = False
    cancellation: bool = True


class AgentCard(BaseModel):
    id: str
    name: str
    version: str
    description: str
    endpoints: Dict[str, str]
    capabilities: AgentCapabilities
    skills: List[SkillDefinition]
    authentication: Dict[str, Any]


raw_card = {
    "id": "agent-fx-01",
    "name": "FX Hedging Agent",
    "version": "2.1.0",
    "description": "Analyzes currency exposure and recommends hedge ratios.",
    "endpoints": {"tasks": "https://api.internal/fx/tasks"},
    "capabilities": {"streaming": True},
    "skills": [{"id": "calc_hedge", "name": "Calculate Hedge", "inputSchema": {"type": "object"}}],
    "authentication": {"type": "bearer"},
}

validated = AgentCard.model_validate(raw_card)
assert validated.id == "agent-fx-01"
assert validated.capabilities.streaming is True
assert len(validated.skills) == 1
assert validated.skills[0].id == "calc_hedge"
```

## Likely follow-ups

- What should an orchestrator do if an Agent Card fails validation?
- How can an orchestrator detect breaking changes in an upgraded Agent Card?

---

[← Q0653](../../batch_07_mcp_a2a_skills_assistants/0653_a2a_agent_card_specification_and_discovery/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0655 →](../../batch_07_mcp_a2a_skills_assistants/0655_a2a_task_state_machine_and_lifecycle/README.md)

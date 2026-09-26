# Q0678 · Progressive disclosure pattern for agent skills

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

Explain the progressive disclosure pattern for agent skills and write Python code implementing two-tier skill loading.

## Answer

Injecting 50 complex skills (each with 2,000 tokens of documentation) into the initial system prompt would consume 100,000 tokens, degrading reasoning and inflating costs.

Progressive Disclosure:
- Tier 1 (Lightweight Index): System prompt includes only name and short 1-line description for each available skill (~50 tokens per skill).
- Tier 2 (On-Demand Activation): When the agent detects relevant user intent, it invokes a `load_skill(skill_name)` tool to retrieve full instructions and tools into the active context.

```python
from typing import Dict, Optional


class ProgressiveSkillLoader:
    def __init__(self):
        self._skills_index: Dict[str, str] = {}
        self._skills_full: Dict[str, str] = {}

    def register_skill(self, name: str, short_desc: str, full_instructions: str):
        self._skills_index[name] = short_desc
        self._skills_full[name] = full_instructions

    def get_system_prompt_catalog(self) -> str:
        lines = ["Available skills (load on-demand via load_skill):"]
        for name, desc in self._skills_index.items():
            lines.append(f"- {name}: {desc}")
        return "\n".join(lines)

    def load_skill(self, name: str) -> Optional[str]:
        return self._skills_full.get(name)


loader = ProgressiveSkillLoader()
loader.register_skill("calc_var", "Calculates portfolio Value at Risk", "# Instructions for VaR calculation...")
loader.register_skill("kyc_check", "Verifies customer KYC verification status", "# KYC verification guidelines...")

catalog = loader.get_system_prompt_catalog()
assert "calc_var: Calculates portfolio" in catalog
assert "# Instructions" not in catalog

full = loader.load_skill("calc_var")
assert full == "# Instructions for VaR calculation..."
```

## Likely follow-ups

- What happens if the agent selects the wrong skill from the short description?
- How should skills be unloaded when a multi-task conversation shifts to a new topic?

---

[← Q0677](../../batch_07_mcp_a2a_skills_assistants/0677_anatomical_structure_of_an_enterprise_agent_skill/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0679 →](../../batch_07_mcp_a2a_skills_assistants/0679_loading_skills_on_demand_based_on_user_intent/README.md)

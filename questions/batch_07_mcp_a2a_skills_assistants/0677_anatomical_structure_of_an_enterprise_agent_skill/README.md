# Q0677 · Anatomical structure of an enterprise Agent Skill

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

Describe the directory layout and components of a standardized enterprise Agent Skill folder (e.g. `skills/fx_hedging/`).

## Answer

A production Agent Skill layout standardizes documentation, code, and interfaces:

```
skills/fx_hedging/
├── SKILL.md             # Required: YAML frontmatter (name, description, triggers) + markdown instructions
├── schemas/
│   ├── input.json       # JSON Schema for skill input parameters
│   └── output.json      # JSON Schema for generated artifacts
├── tools/
│   ├── get_spot_rates.py
│   └── calculate_exposure.py
├── scripts/
│   └── run_stress_test.py
└── references/
    └── hedging_policy_2026.md
```

Components:
- `SKILL.md`: Frontmatter parsed by the orchestrator; body injected into agent context upon activation.
- `schemas/`: Machine-validated interface boundaries.
- `tools/`: MCP-compatible or local functions callable by the model while executing this skill.
- `references/`: Passive domain documentation accessible as MCP resources.

## Likely follow-ups

- How does standardizing skill structure improve developer onboarding?
- How does an orchestrator scan the filesystem to build its skill catalog?

---

[← Q0676](../../batch_07_mcp_a2a_skills_assistants/0676_what_is_an_agent_skill_and_how_does_it_differ_from_a_tool/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0678 →](../../batch_07_mcp_a2a_skills_assistants/0678_progressive_disclosure_pattern_for_agent_skills/README.md)

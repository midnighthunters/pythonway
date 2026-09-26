# Q0676 · What is an Agent Skill and how does it differ from a Tool

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Easy |

## Question

What is an Agent Skill, and how does it differ architecturally from an individual Tool?

## Answer

An Agent Skill is a high-level, cohesive bundle of instructions, domain knowledge, scripts, and tools packaged together to solve a specific business capability.

Comparison:
1. Granularity:
   - Tool: A single executable function (e.g. `query_database(sql)` or `send_email(to, body)`).
   - Skill: A composite capability (e.g. `ReconcileTradeBreaksSkill` containing prompt instructions, domain guidelines, a workflow state machine, and several tools like DB query, FX converter, and booking API).
2. Packaging:
   - Skills are typically organized as modular directories containing:
     - `SKILL.md`: Core system instructions, rules, and few-shot examples.
     - `tools/`: Underlying tool schemas and handlers.
     - `scripts/`: Deterministic execution scripts.
     - `resources/`: Domain reference tables and templates.
3. Progressive Disclosure:
   - Tools are often loaded wholesale into the LLM context.
   - Skills can be indexed as brief summaries in the system prompt and loaded in detail only when the user's intent activates the skill.

## Likely follow-ups

- Why is packaging capabilities as skills easier for enterprise domain teams to maintain?
- Can a skill invoke other skills?

---

[← Q0675](../../batch_07_mcp_a2a_skills_assistants/0675_evaluating_performance_and_communication_cost_in_a2a_swarms/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0677 →](../../batch_07_mcp_a2a_skills_assistants/0677_anatomical_structure_of_an_enterprise_agent_skill/README.md)

# Q0484 · Tool selection at scale

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Tooling | Medium |

## Question

The platform has 400 tools from many MCP servers. How do you keep agents choosing the right tools?

## Answer

- Don't load everything: select a candidate set per request (by assistant configuration, user role and embedding search over the tool descriptions), typically 5–30 tools.
- Namespace and curate: server or domain prefixes (`hr.search_policies`), no near-duplicates, and deprecate overlapping tools.
- Description quality: when to use it and when not to, with examples, reviewed like prompts and tested with tool-selection evaluations.
- Hierarchy: a "find tools" meta-tool or skill packs, loaded on demand when the agent realises it needs a capability.
- Routing: specialist agents with small tool sets rather than one agent with everything.
- Stable ordering and schemas help prompt caching (the MCP 2026-07-28 guidance recommends deterministic tool list order).
- Measure it: tool-selection accuracy per tool, confusion pairs, "no suitable tool" rates, and tools never used (remove them).

## Likely follow-ups

- How would you detect that two tools are being confused?

---

[← Q0483](../../batch_05_agentic_patterns_orchestration/0483_judging_the_quality_of_a_task_decomposition/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0485 →](../../batch_05_agentic_patterns_orchestration/0485_load_tools_on_demand/README.md)

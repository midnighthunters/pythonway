# Q0683 · Skill versioning, deprecation and rollback in production

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

How should an enterprise GenAI platform manage semantic versioning, deprecation notices, and emergency rollbacks for Agent Skills?

## Answer

Managing skills in production requires rigorous lifecycle governance:

1. Semantic Versioning (SemVer):
   - `MAJOR`: Breaking changes to skill input/output schemas or required tools.
   - `MINOR`: Backward-compatible new features (e.g. new optional fields).
   - `PATCH`: Internal prompt tweaks, bug fixes, or documentation clarifications.
2. Deprecation Header: When a skill is deprecated, the registry returns a warning in the metadata (`deprecated: true, migrate_to: "fx_hedging_v2"`).
3. Concurrent Version Serving: Maintain versioned endpoints (`skills/v1/calc_var` and `skills/v2/calc_var`) so in-flight workflows do not break.
4. Instant Rollback: Registry configurations point aliases (e.g. `current`) to tested semantic tags. If v2 exhibits hallucinations, alias `current` is instantly repointed to v1 without code deployments.

## Likely follow-ups

- Why are LLM prompts sensitive to minor wording changes across skill versions?
- How should regression testing be structured before promoting a skill version?

---

[← Q0682](../../batch_07_mcp_a2a_skills_assistants/0682_skill_composition_combining_multiple_skills_for_compound/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0684 →](../../batch_07_mcp_a2a_skills_assistants/0684_auditing_skill_inputs_and_generated_artifacts/README.md)

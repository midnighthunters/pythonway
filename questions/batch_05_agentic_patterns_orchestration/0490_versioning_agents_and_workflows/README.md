# Q0490 · Versioning agents and workflows

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Operations | Medium |

## Question

How do you version an agent (prompts, tools, graph, model) so behaviour changes are controlled and traceable?

## Answer

- Treat the agent as a release artefact: the graph or code version, prompt versions, the tool set and schema versions, the model and deployment versions, guardrail policies and the parameters, combined into one agent version (a manifest), stored in the registry.
- Every run records the agent version (and its component versions) in its state and traces.
- Changes go through CI: unit tests, control-flow tests with fakes, an evaluation gate on scenario suites, and a security review for new tools or permissions.
- Rollout: canary by traffic share or tenant, with automatic comparison, and a rollback that repoints the version.
- Compatibility: tool schemas are versioned (additive changes are preferred), and state schemas are versioned with migrations for in-flight runs.
- Documentation: a changelog per version for model-risk and audit, including why the change was made and its evaluation results.

## Likely follow-ups

- What's the difference between versioning a prompt and versioning an agent?

---

[← Q0489](../../batch_05_agentic_patterns_orchestration/0489_replay_an_agent_run_for_debugging/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0491 →](../../batch_05_agentic_patterns_orchestration/0491_migrating_in_flight_runs_across_versions/README.md)

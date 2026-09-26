# Q0414 · Hierarchical agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Multi-agent | Medium |

## Question

When would you use a hierarchy of agents (a supervisor of supervisors), and what are the risks?

## Answer

Use it when a task spans several domains, each with its own tools and expertise, for example an operations agent delegating to a payments team supervisor (with reconciliation and investigation workers) and a comms team supervisor (with drafting and approval workers). Each level keeps a manageable context and tool set, and teams can own their sub-hierarchies.

Risks:
- Latency and cost multiply with depth (each level adds LLM calls).
- Information loss: summaries passed up and down drop details, and misinterpretations compound ("telephone game").
- Harder debugging and evaluation (nested trajectories).
- Accountability and permissions become unclear if sub-agents act with the top-level agent's authority.

Mitigations: keep the hierarchy shallow (usually two levels), use structured handoff and result schemas, apply per-level budgets, scope permissions per sub-agent, trace end to end, and evaluate each level separately.

## Likely follow-ups

- How would you decide whether a sub-task deserves its own sub-agent?

---

[← Q0413](../../batch_05_agentic_patterns_orchestration/0413_supervisor_multi_agent_pattern/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0415 →](../../batch_05_agentic_patterns_orchestration/0415_handoffs_versus_agents_as_tools/README.md)

# Q0402 · Workflows versus agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent design | Medium |

## Question

When should you build a deterministic workflow (the code decides the steps) instead of an autonomous agent (the model decides)?

## Answer

Prefer a workflow when:
- The steps are known and stable (classify, then extract, then validate, then file). It is more predictable, testable, cheaper and easier to audit, which suits regulated processes.
- Errors are costly, and every path must be reviewed and approved in advance.
- Latency and cost budgets are tight.

Prefer an agent when:
- The task is open-ended or varies a lot (research, troubleshooting, multi-system investigation).
- The number and order of steps depend on what is discovered along the way.
- Tools are many and combinations are hard to enumerate.

The common middle ground is a workflow with agentic nodes: a graph (for example LangGraph) where most edges are fixed, and specific nodes let the model choose among limited tools, with explicit approval nodes for side effects. Start with the simplest thing that works, and add autonomy only where evaluation shows it pays off.

## Likely follow-ups

- How would you convert an agent that works in the demo into something auditable?

---

[← Q0401](../../batch_05_agentic_patterns_orchestration/0401_what_makes_a_system_agentic/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0403 →](../../batch_05_agentic_patterns_orchestration/0403_anatomy_of_an_agent_loop/README.md)

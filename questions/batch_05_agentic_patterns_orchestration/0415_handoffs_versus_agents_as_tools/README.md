# Q0415 · Handoffs versus agents-as-tools

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Multi-agent | Medium |

## Question

Compare two ways of combining agents: handing off control of the conversation to another agent, versus calling another agent as a tool and getting its result back.

## Answer

Handoff (transfer control):
- The receiving agent takes over the conversation with the user, for example triage handing off to a billing specialist.
- Good when the specialist needs its own multi-turn dialogue, tools and persona.
- Risks: loss of context unless it's passed explicitly, ping-pong handoffs, and the user noticing inconsistent behaviour.

Agent-as-tool (delegate and return):
- The orchestrator calls the sub-agent with a task and gets a result back, and it stays in charge of the conversation.
- Good for bounded sub-tasks (research this, draft that) and parallel fan-out.
- The orchestrator keeps a consistent voice and can combine results. The costs are nested latency, and results that must be summarised.

Rule of thumb: use agents-as-tools for sub-tasks, and handoffs when the user should interact with the specialist directly. Both need structured payloads, budgets, tracing, and permission checks at the boundary. Across services, A2A formalises agent-to-agent tasks, and MCP formalises tools.

## Likely follow-ups

- Which pattern makes audit trails easier, and why?

---

[← Q0414](../../batch_05_agentic_patterns_orchestration/0414_hierarchical_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0416 →](../../batch_05_agentic_patterns_orchestration/0416_handoff_loop_with_ping_pong_protection/README.md)

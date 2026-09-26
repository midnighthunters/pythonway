# Q0468 · Cost of multi-agent systems

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Cost control | Medium |

## Question

A multi-agent prototype costs 15 times more per task than a single-agent version. Where does the cost come from, and how do you reduce it?

## Answer

Sources:
- More LLM calls: supervisor hops, planning, critique rounds, and each worker's own reasoning loop.
- Context duplication: every agent receives the system prompt, tool schemas and often the shared history, so tokens multiply with agents and turns.
- Verbose inter-agent messages: agents "chatting" in prose, with full transcripts passed around.
- Retries and loops multiplied across agents, and reasoning models used everywhere.

Reductions:
- Collapse agents where evaluation shows no benefit. Use tools or simple functions instead of agents for deterministic steps.
- Structured, compact handoffs (summaries plus ids, not transcripts), and sub-agents that return only results.
- Model tiering: small models for routing and extraction, large ones only for hard reasoning.
- Prompt caching of the shared stable prefixes, and trimming tool schemas per agent.
- Budgets per run and per agent, and caps on critique and re-planning rounds.
- Measure cost per successful task: sometimes the extra cost buys real success-rate gains, and sometimes it doesn't.

## Likely follow-ups

- How would you decide whether a critic agent is paying for itself?

---

[← Q0467](../../batch_05_agentic_patterns_orchestration/0467_observability_requirements_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0469 →](../../batch_05_agentic_patterns_orchestration/0469_when_multi_agent_is_overkill/README.md)

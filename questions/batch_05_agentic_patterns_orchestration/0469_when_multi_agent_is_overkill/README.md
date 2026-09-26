# Q0469 · When multi-agent is overkill

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent design | Medium |

## Question

A team wants six cooperating agents for a policy Q&A assistant. How do you push back constructively?

## Answer

Ask what each agent adds that a single, well-scoped agent or workflow doesn't:
- Policy Q&A is retrieval, then grounded answer, then citation check. That is a fixed pipeline with maybe one agentic retrieval step. Six agents add latency (sequential hops), cost (duplicated context), failure points (handoff errors, loops) and a harder evaluation (nested trajectories), with little benefit.

Multi-agent designs pay off when there are:
- Genuinely distinct skill and tool sets with separate permissions (payments versus communications).
- Parallelisable independent sub-tasks (analyse 30 contracts).
- Separate ownership (different teams own different agents, possibly across A2A boundaries).
- Context isolation needs (long, noisy sub-tasks).

Constructive path: build the simplest baseline, build the evaluation set, and add an agent only when the evaluation shows a measurable gain that justifies its cost and complexity.

## Likely follow-ups

- What metric would you use to justify adding the second agent?

---

[← Q0468](../../batch_05_agentic_patterns_orchestration/0468_cost_of_multi_agent_systems/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0470 →](../../batch_05_agentic_patterns_orchestration/0470_orchestrating_a_personal_ai_assistant/README.md)

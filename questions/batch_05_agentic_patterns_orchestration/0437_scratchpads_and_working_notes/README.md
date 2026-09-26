# Q0437 · Scratchpads and working notes

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Context engineering | Medium |

## Question

What is an agent scratchpad or notes file, and why do long-running agents benefit from explicit note-taking?

## Answer

- A scratchpad is structured working memory the agent writes to deliberately: the goal, a plan with checkboxes, key findings with sources, decisions made, and open questions. It can be a state field or a file the agent reads and updates through tools.
- Why it helps: long runs overflow the context. Trimming or summarising the transcript loses details, while a curated notes file keeps what matters. It reduces repeated work ("already checked the vendor API"), helps the agent resume after interruptions or handoffs, and gives humans a readable view of progress.
- Practices: a fixed schema (goal, plan, facts, decisions, todo), size limits, updates at milestones rather than every step, citations for facts, and never storing secrets.

Coding agents often use this pattern with a progress or todo file. Personal assistants use it for multi-day tasks.

## Likely follow-ups

- What should happen to the scratchpad when a run finishes?

---

[← Q0436](../../batch_05_agentic_patterns_orchestration/0436_episodic_memory_retrieval_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0438 →](../../batch_05_agentic_patterns_orchestration/0438_summarise_tool_outputs_between_steps/README.md)

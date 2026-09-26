# Q0501 · What LangGraph is and why use it

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph foundations | Easy |

## Question

What is LangGraph, and why would a team building agents on an enterprise platform choose it?

## Answer

LangGraph is a low-level orchestration framework and runtime for stateful, long-running LLM applications. You model the application as a graph: a typed shared state, nodes (functions that read the state and return updates) and edges (fixed or conditional transitions, including loops).

Why teams choose it:
- Explicit control flow: you decide which parts are deterministic workflow and which are agentic, which makes it auditable and testable.
- Durable execution: checkpointers persist the state after every step, so runs survive crashes and can pause for hours (human approval) and resume.
- Human-in-the-loop as a first-class feature: `interrupt()` pauses anywhere and resumes with `Command(resume=...)`.
- Streaming of state updates, LLM tokens and custom events for responsive UIs.
- Time travel: inspect, replay and fork past checkpoints for debugging.
- Multi-agent building blocks: subgraphs, `Send` for fan-out, `Command` for handoffs.
- Model- and tool-agnostic. It reached a stable 1.x API, and LangChain 1.x's `create_agent` runs on it.

## Likely follow-ups

- When would LangGraph be overkill?

---

[← Q0500](../../batch_05_agentic_patterns_orchestration/0500_whiteboard_disruption_recovery_with_cooperating_agents/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0502 →](../../batch_06_langgraph_langchain/0502_langgraph_versus_langchain/README.md)

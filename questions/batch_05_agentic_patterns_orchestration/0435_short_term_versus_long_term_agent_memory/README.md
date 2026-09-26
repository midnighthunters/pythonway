# Q0435 · Short-term versus long-term agent memory

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Memory | Easy |

## Question

Distinguish the kinds of memory an agent uses, and where each is stored.

## Answer

- Working (short-term) memory: the current run's messages, tool results and scratch state, held in the context window and in checkpointed state (for example a LangGraph thread). It is trimmed or summarised as it grows.
- Episodic memory: records of past runs (task, actions, outcome, lessons), retrieved when a similar task appears ("last time, the vendor API needed the ISO date format").
- Semantic memory: durable facts and preferences about the user or domain ("home office is Canary Wharf"), stored in a key-value or document store (for example the LangGraph Store), with namespaces per user.
- Procedural memory: how to do things, such as system prompts, skills and tool descriptions, often versioned as code or configuration. Some systems let agents propose updates to it, with review.

Design points: scope everything per user and tenant, add provenance and TTLs, let users see and delete their memories, retrieve memory selectively (not all of it every turn), and guard against poisoning (only write memories from trusted signals).

## Likely follow-ups

- Which memory type is most dangerous to let the agent update itself?

---

[← Q0434](../../batch_05_agentic_patterns_orchestration/0434_event_sourced_agent_state/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0436 →](../../batch_05_agentic_patterns_orchestration/0436_episodic_memory_retrieval_for_agents/README.md)

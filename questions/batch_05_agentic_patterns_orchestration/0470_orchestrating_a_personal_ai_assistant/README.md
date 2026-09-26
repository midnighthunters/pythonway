# Q0470 · Orchestrating a personal AI assistant

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Personal assistants | Medium |

## Question

Design the orchestration for a personal AI assistant that handles email, calendar, documents and internal apps for an employee.

## Answer

- Entry: a chat or voice UI, plus background triggers (new email, a calendar change, schedules).
- Orchestrator: an intent router, then a small set of skills or sub-agents (inbox triage, scheduling, document Q&A, expenses, travel), each with a scoped tool set. Tools are exposed through MCP servers behind a governed gateway (Graph or email, calendar, document management, HR and finance systems).
- Identity: acts on behalf of the user (delegated OAuth tokens with narrow scopes), and entitlement checks happen in every downstream system.
- Memory: per-user preferences and facts (inspectable and deletable), episodic lessons, and a per-task scratchpad.
- Autonomy tiers: read and summarise automatically; draft and propose need user confirmation; send, book or pay need explicit approval; some actions are never allowed.
- Safety: untrusted content (emails, documents) is treated as data (injection defences, no tool authority from content), outputs are filtered, and every action is audited.
- Proactivity: notifications with explanations and undo, quiet hours, and rate limits.
- Operations: per-user budgets, tracing, evaluation of each skill, and a kill switch.

## Likely follow-ups

- How would you stop a malicious email from making the assistant forward confidential files?

---

[← Q0469](../../batch_05_agentic_patterns_orchestration/0469_when_multi_agent_is_overkill/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0471 →](../../batch_05_agentic_patterns_orchestration/0471_design_a_flight_disruption_rebooking_agent/README.md)

# Q0433 · Durable execution for long-running agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Durability | Medium |

## Question

Some agent tasks take hours or days (waiting for approvals, polling external systems). What does "durable execution" mean, and what options exist?

## Answer

Durable execution means the workflow's progress survives process crashes, deployments and long waits: state is persisted after each step, and the workflow resumes exactly where it left off, often on a different machine, without redoing completed steps.

Options:
- Agent frameworks with persistence: LangGraph checkpointers (Postgres) plus a runtime that resumes threads, and its human-in-the-loop interrupts can wait indefinitely.
- Workflow engines: Temporal, AWS Step Functions and Durable Functions on Azure provide timers, retries, signals (for approvals) and event-history replay. LLM calls become activities.
- A queue plus a state store: simple jobs with explicit state machines in a database, driven by messages (SQS, Service Bus, Kafka).

Requirements either way: idempotent steps, deterministic orchestration logic (important for replay-based engines), versioning for in-flight runs, visibility into run status, timeouts for waits, and cancellation.

## Likely follow-ups

- Why must orchestration code be deterministic in replay-based engines such as Temporal?

---

[← Q0432](../../batch_05_agentic_patterns_orchestration/0432_checkpoint_and_resume_agent_runs/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0434 →](../../batch_05_agentic_patterns_orchestration/0434_event_sourced_agent_state/README.md)

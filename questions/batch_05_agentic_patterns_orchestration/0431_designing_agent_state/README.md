# Q0431 · Designing agent state

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | State management | Medium |

## Question

What should an agent's state contain, and how do you design it so the agent is resumable, debuggable and safe?

## Answer

Contents:
- Inputs: the task, the user identity and entitlement context (as a reference, not raw tokens), and configuration versions.
- Conversation or messages (trimmed), and structured working state: the plan, completed steps and their results (or references to large results), open questions, and extracted facts.
- Control fields: step count, budget used, status (running, waiting for approval, failed), pending approvals, retry counters.
- Outputs: the final answer and artifacts, plus an action log.

Design principles:
- Prefer structured fields over parsing transcripts: reducers merge updates predictably (for example "append to messages", "overwrite status").
- Keep it serialisable (JSON-safe), so it can be checkpointed, and small (store large blobs externally with references).
- Never store secrets or raw credentials. Store handles.
- Version the schema, so in-flight runs survive deployments.
- Make updates explicit per step (a node returns a partial update), which makes the history auditable and time-travel debugging possible.

## Likely follow-ups

- Why store references to large tool results rather than the results themselves?

---

[← Q0430](../../batch_05_agentic_patterns_orchestration/0430_risk_tiered_autonomy/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0432 →](../../batch_05_agentic_patterns_orchestration/0432_checkpoint_and_resume_agent_runs/README.md)

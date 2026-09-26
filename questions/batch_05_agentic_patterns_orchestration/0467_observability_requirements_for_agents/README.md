# Q0467 · Observability requirements for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Observability | Medium |

## Question

What must you capture to operate and debug agents in production, beyond normal service telemetry?

## Answer

- The full trajectory per run: every model call (prompt version, model, parameters, tokens, latency, output), every tool call (name, validated arguments or a redacted summary, result status, latency), decisions (routing, re-planning, handoffs) and state snapshots or checkpoints.
- Control events: guard trips (loops, budgets), approvals requested and resolved (by whom), escalations, and policy blocks.
- Outcomes: the final status and stop reason, task success (from verifiers, users or downstream systems), and user feedback.
- Aggregates: steps per run, tool error rates, retry and fallback rates, cost per run and per successful task, and latency per step and end to end.
- Correlation: trace ids propagated across sub-agents, MCP servers and A2A calls, and business ids (the booking or break id) on spans, so support can find the run.
- Replay: enough to re-run a trajectory against fakes for debugging.
- Privacy: redaction, access controls and retention for prompt and tool content.

## Likely follow-ups

- Which three agent metrics would you put on the on-call dashboard?

---

[← Q0466](../../batch_05_agentic_patterns_orchestration/0466_pause_and_resume_an_agent_with_generators/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0468 →](../../batch_05_agentic_patterns_orchestration/0468_cost_of_multi_agent_systems/README.md)

# Q0443 · Stop conditions for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent control | Easy |

## Question

List the stop conditions a production agent needs, and what it should return in each case.

## Answer

- Success: the model produces a final answer that passes validation. Return the answer, evidence and actions.
- Needs input: missing information or ambiguity. Ask the user a specific question and pause (persist the state).
- Needs approval: a pending side effect. Pause with an approval request.
- Budget exhausted: the step, token, cost or time limit is reached. Return partial results with an honest "couldn't finish" and what's left.
- No progress: repeated calls, cycles, or the same failure after re-planning. Stop, summarise attempts, and escalate.
- Policy stop: a guardrail blocked an action, or the request is out of scope. Refuse with an explanation or a redirect.
- Fatal error: a dependency is down (circuit open) or there is an internal error. Return a graceful error with a trace id, and alert if it's systemic.
- User cancellation: stop immediately, cancel in-flight calls, and record the state.

Each stop reason should be a machine-readable status in the response and in traces, so dashboards show why runs end.

## Likely follow-ups

- Which stop reasons should page an on-call engineer?

---

[← Q0442](../../batch_05_agentic_patterns_orchestration/0442_final_answer_schema_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0444 →](../../batch_05_agentic_patterns_orchestration/0444_agent_failure_modes_and_recovery/README.md)

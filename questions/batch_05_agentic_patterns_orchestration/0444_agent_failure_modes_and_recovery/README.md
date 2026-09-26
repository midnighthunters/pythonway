# Q0444 · Agent failure modes and recovery

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Reliability | Medium |

## Question

What are the common ways agents fail in production, and what recovery strategy fits each?

## Answer

- Wrong tool or arguments: validate the arguments, return actionable errors, improve tool descriptions, and reduce the tool set per task.
- Hallucinated results or claims: require evidence tied to tool outputs, verify numbers against tool results, and use structured final answers.
- Loops and no progress: step and repetition guards, cycle detection with a reflection prompt, and re-planning caps.
- Tool and dependency failures: retries with backoff for transient errors, circuit breakers, fallbacks (an alternative tool), and graceful degradation.
- Partial side effects: sagas with compensation, idempotency keys and outboxes.
- Context overflow and drift: compaction, sub-agents, and re-injecting the goal and constraints.
- Prompt injection from tool outputs: least privilege, approvals, isolating untrusted content, and output filtering.
- Premature completion ("done!" when it isn't): verifiers and final-state checks.
- Over-asking the user: better defaults, and clarifying only when it changes the outcome.

Track each failure mode as a labelled category in error analysis, and target the biggest bucket.

## Likely follow-ups

- Which failure mode is hardest to detect automatically?

---

[← Q0443](../../batch_05_agentic_patterns_orchestration/0443_stop_conditions_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0445 →](../../batch_05_agentic_patterns_orchestration/0445_return_tool_errors_the_model_can_act_on/README.md)

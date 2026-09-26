# Q0479 · Guardrails on agent actions

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent safety | Medium |

## Question

Beyond content filters, what guardrails should wrap an agent's actions?

## Answer

- Before the call: tool allowlists per task, argument validation (schema plus business rules), authorisation against the user's entitlements, rate limits and budgets, risk-tier policy (auto, approve or forbid), and checks that inputs come from trusted sources (not injected instructions).
- During the call: timeouts, circuit breakers, idempotency keys, a sandbox for code and browsing, and network egress restrictions.
- After the call: verification that the effect matches the intent (re-read the state), anomaly detection on action patterns (for example 50 emails in a minute), and output filtering of tool results before they reach users.
- Across the run: step and cost caps, loop detection, audit logging, a human-escalation path, and a kill switch per agent or tenant.

The principle: the model proposes, deterministic code disposes. Guardrails live in the tool dispatcher and platform, not in the prompt, so they hold even when the model is confused or manipulated.

## Likely follow-ups

- Which guardrail would have stopped the most incidents in agent systems you know of?

---

[← Q0478](../../batch_05_agentic_patterns_orchestration/0478_explainable_risk_score_aggregation/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0480 →](../../batch_05_agentic_patterns_orchestration/0480_policy_engine_for_tool_calls/README.md)

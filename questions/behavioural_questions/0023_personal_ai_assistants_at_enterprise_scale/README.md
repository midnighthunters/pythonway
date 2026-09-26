# B0023 · Personal AI assistants at enterprise scale

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Product thinking | Hard |

## Question

The JD mentions personal AI assistants. What does it take to give every employee a personal assistant safely?

## Answer

- Identity and delegation: the assistant acts on behalf of one user with exactly that user's entitlements (on-behalf-of tokens, scoped consent), never broader.
- Memory: per-user long-term memory (preferences, facts) that the user can inspect and delete, kept separate from shared knowledge.
- Tools: email, calendar, documents and internal apps through governed connectors (MCP servers behind a gateway), least privilege, approval before side effects.
- Proactivity: scheduled and background tasks with durable execution, notifications, and rate and cost caps.
- Safety: prompt-injection defences for content read from email and documents, an audit trail of actions, a kill switch.
- Scale: tenant isolation, quotas, cost per user, latency budgets.
- UX: explain what it did and why, and make undo easy.

## Likely follow-ups

- How do you stop the assistant leaking one user's data to another?
- What happens when a malicious email contains instructions for the assistant?

---

[← B0022](../../behavioural_questions/0022_agent_use_cases_for_corporate_functions/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0024 →](../../behavioural_questions/0024_how_regulation_shapes_ai_delivery_in_a_bank/README.md)

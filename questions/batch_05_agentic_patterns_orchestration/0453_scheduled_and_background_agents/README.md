# Q0453 · Scheduled and background agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Event-driven agents | Medium |

## Question

A personal assistant should run background jobs (a morning briefing, monitoring subscriptions for price rises). What changes when an agent runs without a user present?

## Answer

- Identity: the job acts on behalf of the user with delegated, scoped credentials (refresh tokens with limited scopes), not a shared service account. Re-check consent and entitlements on each run.
- No live approval: anything needing confirmation becomes a notification ("I found a price rise; cancel the subscription?") rather than an action. Only pre-authorised low-risk actions run automatically.
- Durability: scheduled triggers (cron, EventBridge, Logic Apps), durable state, retries, and idempotency (a job must not run twice for the same slot).
- Cost and fairness: per-user budgets, and jitter so millions of 07:00 briefings don't hit providers at the same second.
- Notifications: deduplicate, throttle, respect quiet hours, and give clear explanations with a one-click undo or opt-out.
- Observability: per-job status, failure alerts, and user-visible history ("what did my assistant do today?").

## Likely follow-ups

- How would you prevent a background agent from spamming a user after a bug?

---

[← Q0452](../../batch_05_agentic_patterns_orchestration/0452_queue_triggered_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0454 →](../../batch_05_agentic_patterns_orchestration/0454_locks_when_agents_share_resources/README.md)

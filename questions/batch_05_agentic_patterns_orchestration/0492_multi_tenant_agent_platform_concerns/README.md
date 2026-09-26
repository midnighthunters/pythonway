# Q0492 · Multi-tenant agent platform concerns

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Platform architecture | Medium |

## Question

LLM Suite hosts agents for many business lines. What must a multi-tenant agent platform provide?

## Answer

- Isolation: per-tenant state, memory, checkpoints, vector indexes and caches, and strict tenant scoping in every data access (enforced in a data-access layer). Information barriers where needed.
- Identity and authorisation: user and agent identities, on-behalf-of tokens to downstream systems, and tenant-specific tool catalogues and policies.
- Quotas and fairness: per-tenant token, cost and concurrency limits, fair scheduling of background jobs, and protection from noisy neighbours.
- Configuration: tenant-level assistants, prompts, models, guardrail policies and autonomy tiers, with guardrails that tenants can tighten but never loosen below the platform minimum.
- Observability and chargeback: per-tenant metrics, traces, cost reports and alerting.
- Governance: per-tenant evaluation gates, model-risk records, audit logs, data retention and deletion.
- Reliability: bulkheads (one tenant's runaway agent can't exhaust shared workers), priority tiers and regional deployment for data residency.

## Likely follow-ups

- Which of these controls must the platform enforce rather than trust tenants to implement?

---

[← Q0491](../../batch_05_agentic_patterns_orchestration/0491_migrating_in_flight_runs_across_versions/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0493 →](../../batch_05_agentic_patterns_orchestration/0493_slos_for_agents/README.md)

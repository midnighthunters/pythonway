# B0026 · What operational excellence means to you

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | JPMC culture | Medium |

## Question

What does operational excellence mean to you as a software engineer? Give an example.

## Answer

- Definition: systems that behave predictably in production, and a team that learns from every failure.
- Practices: SLOs with error budgets, dashboards and actionable alerts, runbooks, safe releases (canary, feature flags, fast rollback), tests that cover failure paths, capacity and cost reviews, blameless postmortems with tracked actions, automating toil.
- GenAI specifics: evaluation gates on prompt and model changes, token and cost monitoring, provider fallback, guardrail metrics.
- Example (STAR): "Our agent service timed out every week. I added per-dependency timeouts and a circuit breaker, a time-to-first-token SLO and a runbook. Pages fell from six a month to one, and MTTR from 90 to 20 minutes."

## Likely follow-ups

- How do you choose SLO targets?
- What is the difference between monitoring and observability?

---

[← B0025](../../behavioural_questions/0025_technology_controls_in_a_bank/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0027 →](../../behavioural_questions/0027_client_service_for_an_internal_platform/README.md)

# B0096 · How you document your work

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Engineering practice | Easy |

## Question

How do you document the systems you build?

## Answer

- README: purpose, quick start, how to run tests and deploy.
- Architecture overview: diagram, key flows, dependencies, data classification.
- ADRs: each decision with context, options and consequences.
- API docs: OpenAPI generated from FastAPI, with examples and error codes.
- Runbooks: alert → diagnosis → mitigation steps → escalation contacts.
- Prompt and model cards: versions, intended use, evaluation results, limitations.
- Keep docs next to the code, review them in PRs, and delete stale ones.

## Likely follow-ups

- How do you keep documentation current?
- What makes a runbook useful at 3 a.m.?

---

[← B0095](../../behavioural_questions/0095_production_ready_for_an_agentic_capability/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0097 →](../../behavioural_questions/0097_rolling_out_an_agent_feature_to_50_000_users/README.md)

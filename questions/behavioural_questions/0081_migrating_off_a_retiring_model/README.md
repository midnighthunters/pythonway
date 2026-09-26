# B0081 · Migrating off a retiring model

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Platform operations | Medium |

## Question

A model your feature depends on will be retired in 60 days. How do you plan the migration?

## Answer

- Inventory: which features, prompts and tenants use it, traffic volumes, and special capabilities relied on (tool calling, JSON output, context length).
- Candidates: shortlist by capability, cost, latency and availability in the required regions and deployment types; check quota.
- Evaluate: run the regression suites (task metrics, format adherence, safety) and tune prompts per candidate.
- Roll out: shadow traffic → canary percentage → full, behind flags, watching quality, latency and cost, with a rollback path.
- Communicate: consumer teams, dates, updated docs.
- Prevent surprises: a model abstraction, version pinning, evaluations that can run at any time, and tracking of provider lifecycle notices (Azure OpenAI and Bedrock both publish retirement dates).

## Likely follow-ups

- What if no replacement matches the quality?
- How do you avoid being surprised by retirements?

---

[← B0080](../../behavioural_questions/0080_ensuring_auditability/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0082 →](../../behavioural_questions/0082_ethically_questionable_ai_use_case/README.md)

# Q0067 · Model version pinning and deprecation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Operations | Medium |

## Question

Providers retire models and update aliases. How do you manage model versions on an enterprise platform?

## Answer

- Pin explicit model versions (or deployment versions) in configuration. Never let production silently follow a floating alias. In Azure OpenAI, control the deployment's version and auto-upgrade policy. In Bedrock, use explicit model IDs or inference profiles.
- Keep a model registry: capabilities, context limits, pricing, approved data classes, owners, and retirement dates.
- Treat an upgrade as a change: run the evaluation suite (quality, safety, format adherence, latency, cost), shadow or canary it, then roll out with a feature flag and a rollback path.
- Maintain per-model prompt variants where behaviour differs.
- Track provider retirement notices and plan migrations well ahead, keeping model-risk documentation current.
- Log the model version with every request for audit and incident analysis.

## Likely follow-ups

- What would you do if a provider retires a model with two weeks' notice?

---

[← Q0066](../../batch_01_llm_fundamentals/0066_open_weight_versus_hosted_models_in_a_bank/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0068 →](../../batch_01_llm_fundamentals/0068_sustainable_request_rate_from_token_quotas/README.md)

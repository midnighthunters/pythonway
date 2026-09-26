# B0089 · Primary model endpoint failing

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Scenario | Medium |

## Question

The primary model endpoint starts failing during London business hours. Walk me through your response.

## Answer

- Detect and declare: alerts on error rate and latency; open an incident and assign roles (incident commander, communications, operations).
- Assess: scope (one deployment, region or model?), error type (5xx, 429 quota, timeouts, content-filter changes), recent changes (deploys, config, the provider status page).
- Mitigate fast: fail over to a secondary deployment, region or provider through routing config; shed non-critical traffic such as batch jobs; enable a degraded mode; show a banner or status-page notice.
- Communicate: regular stakeholder updates and a ticket with the provider.
- Recover and learn: verify, unwind mitigations gradually, run a postmortem, and improve automatic failover, runbooks and quota headroom.

## Likely follow-ups

- How should automatic failover decide to trigger?
- What are the risks of failing over to a different model?

---

[← B0088](../../behavioural_questions/0088_onboarding_a_new_model_to_the_platform/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0090 →](../../behavioural_questions/0090_inheriting_a_flaky_untested_service/README.md)

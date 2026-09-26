# B0066 · A mistake you made in production

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - accountability | Medium |

## Question

Tell me about a mistake you made that reached production.

## Answer

- Own it: e.g. a config change disabled a tenant's rate limit and caused a cost spike.
- Response: detected by a cost alert, rolled back, notified stakeholders, quantified the impact.
- Prevention: config validation in CI, staged config rollout, peer review for config changes, better alert thresholds.
- Reflection: treat configuration as code.

Keep it honest and specific, and focus on what you learned.

## Likely follow-ups

- How was it detected?
- What did the team change as a result?

---

[← B0065](../../behavioural_questions/0065_pushing_back_on_an_unrealistic_estimate/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0067 →](../../behavioural_questions/0067_automating_a_manual_process/README.md)

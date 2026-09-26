# B0054 · Found an error others had missed

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - attention to detail | Medium |

## Question

Tell me about a time you found an error that others had missed.

## Answer

- Situation: while reviewing a usage report used for chargeback, you noticed timezone-naive timestamps that double-counted usage around daylight-saving changes.
- Action: reproduced it with a test, quantified the impact (about 3% overbilling to two business units), raised it privately with the owner, fixed it with timezone-aware UTC storage, added DST boundary tests, and sent corrected figures to the finance partners.
- Result: accurate chargeback and a new CI check.

Emphasise verifying before raising, respectful communication and a systemic fix.

## Likely follow-ups

- How did you raise it without embarrassing the author?
- What habits help you catch issues like this?

---

[← B0053](../../behavioural_questions/0053_production_incident_you_handled/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0055 →](../../behavioural_questions/0055_asked_to_skip_a_required_control/README.md)

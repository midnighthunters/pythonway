# B0053 · Production incident you handled

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - incidents | Medium |

## Question

Describe a production incident you handled and what you changed afterwards.

## Answer

Show a calm sequence: contain, communicate, fix, prevent.

- Situation: after a provider model update, structured outputs stopped parsing and 30% of requests failed.
- Action: declared an incident; mitigated by pinning the previous model version and rolling back the prompt with a feature flag; posted updates every 30 minutes; found the root cause (schema adherence changed); fixed with strict structured outputs plus validation and repair; verified on a canary.
- Result: mitigated in 25 minutes, resolved in three hours, no data loss.
- Afterwards: blameless postmortem; model-version pinning, contract tests on output schemas, an evaluation gate for model upgrades, an alert on parse-failure rate, and incident documentation for the audit trail.

In a bank, prevention and documentation land better than heroics.

## Likely follow-ups

- How did you keep users informed during the incident?
- What was the root cause behind the root cause?

---

[← B0052](../../behavioural_questions/0052_iterating_quickly_on_feedback/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0054 →](../../behavioural_questions/0054_found_an_error_others_had_missed/README.md)

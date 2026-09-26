# B0052 · Iterating quickly on feedback

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - delivery | Medium |

## Question

Tell me about a time you took something from prototype to production by iterating quickly on feedback.

## Answer

The JD mentions "iterating quickly with feedback".

- Situation: a policy-summarisation tool whose pilot users found the summaries too generic.
- Action: shipped a thin prototype in a week to ten pilot users behind a flag; captured feedback (ratings plus comments); ran weekly iterations adding section-aware chunking, citations and a "key obligations" format; built an evaluation set from real user examples; hardened for production (auth, rate limits, logging, runbook) before a wide rollout.
- Result: satisfaction 3.1 → 4.4 out of 5, rollout to 2,000 users, no Sev-1 incidents.

The point is the balance: fast learning loops, then production discipline before scaling.

## Likely follow-ups

- How did you decide it was ready for production?
- Which feedback did you choose not to act on?

---

[← B0051](../../behavioural_questions/0051_solving_a_hard_problem_creatively/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0053 →](../../behavioural_questions/0053_production_incident_you_handled/README.md)

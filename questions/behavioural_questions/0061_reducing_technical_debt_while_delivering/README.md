# B0061 · Reducing technical debt while delivering

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - engineering quality | Medium |

## Question

Tell me about a time you reduced technical debt while still delivering features.

## Answer

- Situation: LLM-calling code was duplicated across services, each with its own retry logic and inconsistent logging.
- Action: quantified the cost (incidents, time per change), proposed an incremental refactor into a shared client library (retries, timeouts, logging, tracing), wrote tests first, migrated service by service behind feature flags, and applied the "leave it better" rule during feature work.
- Result: shorter lead time for changes, no more incidents from inconsistent retries, and features kept shipping.

## Likely follow-ups

- How did you justify the time to the product owner?
- How do you decide which debt to pay down first?

---

[← B0060](../../behavioural_questions/0060_prioritising_competing_urgent_tasks/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0062 →](../../behavioural_questions/0062_improving_reliability_of_a_system/README.md)

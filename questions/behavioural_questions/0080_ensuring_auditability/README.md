# B0080 · Ensuring auditability

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Regulated environment | Medium |

## Question

How do you make the systems you build auditable?

## Answer

- Structured, immutable audit events: who, what, when and why. Include user identity, action, inputs and outputs (or redacted versions or hashes), model and prompt versions, tool calls, approvals, and correlation IDs across services.
- Tamper evidence: append-only storage (WORM or object lock), hash chaining, restricted access, retention per policy.
- Reproducibility: version code, prompts, model versions, retrieval index snapshots and configuration, and record decoding parameters.
- Change evidence: PR reviews, pipeline logs and approvals linked to tickets.
- Queryable: audit data in a searchable store that is reviewed regularly.
- Privacy balance: redact PII in logs and control access to audit data.

## Likely follow-ups

- How would you reconstruct why an agent took an action last month?
- How do you audit without storing sensitive prompts?

---

[← B0079](../../behavioural_questions/0079_delivering_bad_news_to_stakeholders/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0081 →](../../behavioural_questions/0081_migrating_off_a_retiring_model/README.md)

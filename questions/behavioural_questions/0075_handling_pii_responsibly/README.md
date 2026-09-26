# B0075 · Handling PII responsibly

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Data protection | Medium |

## Question

Tell me about a time you handled sensitive data or PII in a system you built.

## Answer

- Principles: data minimisation, classification, encryption in transit and at rest, least-privilege audited access, redaction or pseudonymisation before data reaches models or logs, retention and deletion rules, and involvement in the DPIA.
- Example: ingestion for HR documents. PII was detected with a recogniser (e.g. Microsoft Presidio) and masked before indexing, retrieval applied entitlement filters, logs were redacted and retention was 90 days.
- Testing: seeded synthetic PII to prove the redaction worked, plus periodic audits.

## Likely follow-ups

- How do you handle PII that ends up in embeddings?
- How do you honour a deletion request across the system?

---

[← B0074](../../behavioural_questions/0074_sending_confidential_data_to_an_unapproved_model/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0076 →](../../behavioural_questions/0076_healthy_dashboards_but_unhappy_users/README.md)

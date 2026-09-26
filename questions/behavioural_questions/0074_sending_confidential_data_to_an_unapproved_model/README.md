# B0074 · Sending confidential data to an unapproved model

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Integrity | Hard |

## Question

A senior stakeholder asks you to send confidential client data to a public, unapproved model API because it gives better results. How do you respond?

## Answer

- Decline, respectfully, and explain why: data classification rules, client confidentiality and vendor risk. An unapproved endpoint lacks the contractual protections on retention, training use and residency.
- Understand the need: what exactly is better (reasoning, context length, a specific capability)?
- Offer approved paths: the same or a similar model through the firm's approved channels (for example Azure OpenAI or Bedrock under enterprise terms via the platform), evaluation on their use case, redaction or pseudonymisation, or a request to onboard the model through the model-approval process.
- If pressed further, escalate and document.

## Likely follow-ups

- How could you legitimately speed up onboarding a new model?
- Which contractual protections matter with model providers?

---

[← B0073](../../behavioural_questions/0073_llm_feature_producing_harmful_outputs/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0075 →](../../behavioural_questions/0075_handling_pii_responsibly/README.md)

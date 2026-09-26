# B0073 · LLM feature producing harmful outputs

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Responsible AI | Hard |

## Question

An LLM feature you built is found to be producing biased or harmful outputs in production. What do you do?

## Answer

- Contain: assess severity and scope; if material, disable or restrict the feature with a kill switch or flag, and add a temporary output filter.
- Communicate: follow the incident process and inform the product owner, risk and compliance, and affected users where appropriate.
- Investigate: collect examples, reproduce, find the cause (prompt, retrieved data, model update, missing guardrail) and measure prevalence with a targeted evaluation set.
- Fix: adjust prompts and instructions, correct data, add moderation guardrails, change the model, or add human review for sensitive outputs.
- Prevent: add the cases to regression and red-team suites, monitor for the pattern, and document everything for audit.

## Likely follow-ups

- How do you measure bias in generative outputs?
- Who decides when the feature can be switched back on?

---

[← B0072](../../behavioural_questions/0072_colleague_committed_a_secret_to_a_repository/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0074 →](../../behavioural_questions/0074_sending_confidential_data_to_an_unapproved_model/README.md)

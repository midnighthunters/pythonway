# B0072 · Colleague committed a secret to a repository

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Integrity | Medium |

## Question

What would you do if you found that a colleague had committed an API key or other secret to a repository?

## Answer

- Treat the secret as compromised immediately, whatever the repository's visibility.
- Follow the incident process: tell the colleague and the owner or security team, and revoke or rotate the secret first. That is the most important step.
- Then remove it from code and history (git filter-repo or BFG), knowing that rewriting history does not un-leak it.
- Check access logs for misuse and document what happened.
- Prevent recurrence blamelessly: pre-commit and server-side secret scanning, a secrets manager or managed identity so there are no keys in code, and a short training note.

## Likely follow-ups

- Why isn't deleting the commit enough?
- How do you avoid static keys entirely on Azure and AWS?

---

[← B0071](../../behavioural_questions/0071_raising_a_security_or_compliance_concern/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0073 →](../../behavioural_questions/0073_llm_feature_producing_harmful_outputs/README.md)

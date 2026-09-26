# Q0196 · Few-shot examples from production data

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Privacy | Medium |

## Question

A team wants to use real past conversations as few-shot examples. What are the risks, and how would you do it safely?

## Answer

Risks:
- Personal or confidential data in examples is shown to other users (the model can repeat it), sent to providers, and stored in logs. It may breach data-minimisation rules and entitlements.
- Examples can carry wrong or outdated answers that get amplified.
- Bias toward the examples' specifics (names, amounts).

Safe approach:
1. Curate a small set, and obtain approval for the data use.
2. De-identify thoroughly (names, accounts, amounts, dates), preferably by rewriting into synthetic but realistic examples.
3. Review the content for correctness and current policy.
4. Store the examples as versioned, reviewed prompt assets, with an owner and expiry.
5. For dynamic selection from a pool, filter by entitlement and scope, and never select across tenants or business lines with information barriers.
6. Evaluate their impact, and prefer instructions over examples when the gain is small.

## Likely follow-ups

- Why is synthetic rewriting safer than simple redaction?

---

[← Q0195](../../batch_02_prompting_context_structured_output/0195_language_control_in_multilingual_replies/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0197 →](../../batch_02_prompting_context_structured_output/0197_choosing_generation_settings_per_task/README.md)

# Q0392 · Guardrail false positives

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Safety evaluation | Medium |

## Question

Users complain the assistant blocks legitimate work (security analysts asking about malware, compliance staff asking about money laundering). How do you measure and reduce guardrail false positives?

## Answer

Measure:
- Build a "benign but sensitive" evaluation set with the affected teams: security research, fraud and AML investigations, HR misconduct policies, medical-leave questions.
- Track the block rate on it, plus production signals (block rate by assistant and team, appeals or "this was wrong" feedback).
- Sample blocked requests (under appropriate access controls) for review.

Reduce:
- Context-aware policies: the same question is allowed for the AML-investigations assistant and its entitled users, and blocked for a general assistant. Pass role and purpose to the guardrail.
- Better classifiers: tuned thresholds per category and language, fine-tuned on in-domain data, and a layered design (cheap classifier first, LLM judge for borderline cases).
- Safe completion instead of refusal: answer at an educational level, or redirect, rather than a hard block.
- An appeal or escalation path, and a fast feedback loop to update the policies.

Track both false positives and false negatives. Loosening without measurement just moves the risk.

## Likely follow-ups

- How do you let the AML team discuss laundering typologies without opening that up to everyone?

---

[← Q0391](../../batch_04_llm_evaluation_observability/0391_choose_a_moderation_classifier_threshold/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0393 →](../../batch_04_llm_evaluation_observability/0393_turn_red_team_findings_into_regression_tests/README.md)

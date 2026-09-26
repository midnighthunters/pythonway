# B0029 · Balancing innovation speed with safety

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Judgment | Medium |

## Question

How do you balance the speed of innovation with safety and risk in GenAI?

## Answer

- Tier by risk: internal read-only drafting is low risk; customer-facing or action-taking agents are high risk. Controls should be proportional.
- Paved road: pre-approved components (gateway, guardrails, logging, evaluation harness) make the safe path the fast path.
- Stage gates: sandbox prototype → limited pilot with human review → wider rollout with monitoring, each gate with explicit criteria (evaluation thresholds, security review).
- Reversibility: feature flags, kill switches, versioned prompts and models, quick rollback.
- Measurement: evaluations and monitoring tell you when it is safe to expand.
- Involve risk partners early; late surprises are what really slow projects down.

## Likely follow-ups

- What evidence would you need to move from pilot to firmwide rollout?
- Give an example where you deliberately slowed something down.

---

[← B0028](../../behavioural_questions/0028_stakeholder_request_that_conflicts_with_policy/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0030 →](../../behavioural_questions/0030_questions_to_ask_the_interviewer/README.md)

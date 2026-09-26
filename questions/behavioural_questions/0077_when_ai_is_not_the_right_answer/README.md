# B0077 · When AI is not the right answer

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Judgment | Medium |

## Question

How do you decide that an LLM or agent is not the right solution?

## Answer

Prefer a simpler solution when:

- Deterministic rules suffice (validation, calculations, routing on known fields): cheaper, testable, explainable.
- Exactness is required (financial or regulatory numbers): compute in code or SQL; an LLM can explain the result but should not calculate it.
- Latency or cost constraints are extreme (very high-QPS paths).
- The data is structured and a search or filter UI solves the need.
- Errors are unacceptable and can't be caught by review.
- The problem itself is unclear, and an LLM would only hide requirement gaps.

LLMs fit unstructured language, variability, drafting, summarisation and fuzzy classification with human review. The best answer is often hybrid: a deterministic workflow with LLM steps.

## Likely follow-ups

- Give an example where you replaced an LLM with plain code.
- How would you handle a stakeholder who wants "AI" regardless?

---

[← B0076](../../behavioural_questions/0076_healthy_dashboards_but_unhappy_users/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0078 →](../../behavioural_questions/0078_challenging_the_status_quo/README.md)

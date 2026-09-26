# Q0477 · Fraud investigation agent design

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent design | Hard |

## Question

Design an agent that helps fraud analysts investigate flagged transactions using payment data, device signals and account history.

## Answer

- Trigger: an alert from the fraud-detection system (rules or ML score) for a transaction or account.
- Evidence gathering (read-only tools): the transaction details, account history and baselines (typical amounts, merchants, geographies), device and IP signals, linked accounts (shared devices or payees), prior alerts and outcomes, and external data (merchant risk lists).
- Analysis: deterministic features and scores from code (velocity, amount z-score, new payee, geo mismatch). The LLM synthesises a narrative: the timeline, which signals fired and why they matter, similar past cases, and gaps in the evidence.
- Output: an explainable risk summary with a score breakdown, recommended actions from a fixed menu (monitor, contact the customer, block the card, file a report), and citations to the evidence. It never takes customer-impacting actions automatically unless a policy explicitly allows it (for example a temporary hold in a clear account-takeover pattern), with immediate analyst review.
- Controls: data minimisation, access logging, analyst decision capture (for model improvement and audit), fairness monitoring (don't use protected attributes, check outcomes across groups), and regulatory reporting requirements handled by humans.

Metrics: analyst time per case, decision accuracy against outcomes, false-positive burden, and consistency across analysts.

## Likely follow-ups

- Which parts of the risk score must never be LLM-generated?

---

[← Q0476](../../batch_05_agentic_patterns_orchestration/0476_code_fix_loop_with_test_feedback/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0478 →](../../batch_05_agentic_patterns_orchestration/0478_explainable_risk_score_aggregation/README.md)

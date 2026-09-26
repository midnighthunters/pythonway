# Q0473 · Trade-break remediation agent

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent design | Hard |

## Question

Operations analysts spend hours clearing trade breaks (mismatches between internal trade records and counterparty confirmations). Design an agent that remediates them safely.

## Answer

- Intake: breaks arrive from the reconciliation system via a queue, with trade, confirm and position data references.
- Investigate (read-only tools): fetch the trade, confirmation, settlement instructions, reference data (SSIs, instrument data), FX rates, and prior similar breaks. The agent compares the fields and classifies the break (price or quantity mismatch, wrong settlement date, missing SSI, duplicate booking, timing difference).
- Decide with playbooks: each break class maps to a deterministic playbook with tolerances (auto-resolve timing differences within T+1; propose a price amendment within tolerance; escalate SSI changes, which are fraud-sensitive). The LLM classifies ambiguous cases, gathers evidence, and drafts communications. It doesn't invent fixes outside the playbooks.
- Act with approval: proposed amendments go to an analyst queue with the evidence and a one-click approve (four-eyes for monetary impact above a threshold). Low-risk actions (tagging, requesting an amended confirm) can be automatic.
- Audit: every step logged with evidence, approver and before and after values. Regulatory records are retained.
- Metrics: the percentage of the daily queue cleared on analyst approval (for example 55%), time to resolve, the error or reversal rate, and analyst overrides.

## Likely follow-ups

- Why must settlement-instruction changes always go to a human?

---

[← Q0472](../../batch_05_agentic_patterns_orchestration/0472_rank_rebooking_options_under_constraints/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0474 →](../../batch_05_agentic_patterns_orchestration/0474_route_exceptions_to_remediation_playbooks/README.md)

# Q0090 · Model documentation for model risk management

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Governance | Medium |

## Question

In a bank, a GenAI use case may fall under model risk management. What documentation and evidence would you prepare for model validation?

## Answer

Frameworks such as US SR 11-7 and the UK PRA's SS1/23 expect models to be inventoried, tiered by risk, validated independently, and monitored. For a GenAI system, prepare:
- Purpose and scope: the use case, users, decisions supported, what is out of scope, and the human-in-the-loop design.
- System description: models and versions, prompts (versioned), retrieval sources and entitlements, tools, guardrails, and the architecture diagram.
- Data: sources, classification, lineage, retention, and any fine-tuning data with approvals.
- Performance evidence: the evaluation dataset and how it was built, metrics and thresholds, results by segment, robustness and adversarial tests, bias and fairness checks where relevant, and known limitations.
- Controls: content filters, PII handling, access control, logging and audit, the change-management process for prompt and model updates, and rollback.
- Monitoring plan: online metrics, drift and quality sampling, incident process, and re-validation triggers (model upgrade, new data source).

Treat this as living documentation, generated and updated from the pipeline where possible.

## Likely follow-ups

- What would trigger re-validation of an already approved assistant?

---

[← Q0089](../../batch_01_llm_fundamentals/0089_explaining_llm_limitations_to_business_stakeholders/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0091 →](../../batch_01_llm_fundamentals/0091_benchmark_contamination/README.md)

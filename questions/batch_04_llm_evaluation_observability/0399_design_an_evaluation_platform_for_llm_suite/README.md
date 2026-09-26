# Q0399 · Design an evaluation platform for LLM Suite

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | System design | Hard |

## Question

Design a shared evaluation platform that hundreds of assistant teams on LLM Suite can use: datasets, runs, judges, gates and online monitoring.

## Answer

Components:
1. Dataset service: versioned datasets (cases, labels, provenance, tags, access controls by data classification), creation from traces, and annotation queues for SMEs.
2. Evaluator library: deterministic metrics (exact and field match, retrieval metrics, format checks), model-graded evaluators (versioned judge prompts and models, calibration records), trajectory and final-state evaluators, and safety suites maintained centrally (red-team and leak probes).
3. Run orchestrator: executes the system under test with manifests (the model, prompt, index and code versions), concurrency and quota-aware scheduling through the LLM gateway, caching, retries, repeated runs, and raw output storage.
4. Results store and analysis: per-case results, slices, comparisons between runs (regressions and fixes), confidence intervals and cost reports.
5. Gates: a policy-as-code per assistant tier (floors, allowed drops, critical tags), integrated with CI/CD and the change-management records.
6. Online evaluation: sampled production traces scored by judges, feedback ingestion, drift monitors and alerts, and links back to datasets.
7. Governance: evidence packs for model-risk validation, audit logs, retention and access controls on sensitive content.

Principles: self-service SDK and templates, platform-owned safety suites that every assistant must pass, and pay-per-use quotas so evaluation load doesn't hurt production.

## Likely follow-ups

- Which evaluations would you make mandatory for every assistant, regardless of team?

---

[← Q0398](../../batch_04_llm_evaluation_observability/0398_evaluating_across_languages/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0400 →](../../batch_04_llm_evaluation_observability/0400_pre_launch_evaluation_plan_for_a_new_assistant/README.md)

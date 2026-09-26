# B0021 · Measuring success of an internal GenAI platform

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Product thinking | Medium |

## Question

How would you measure the success of an internal GenAI platform?

## Answer

Use a balanced scorecard:

- Adoption: DAU/WAU/MAU, share of eligible employees active, retention cohorts, usage of agents and tools.
- Value: time saved (task-level instrumentation plus surveys), tasks completed by agents, business KPIs per use case.
- Quality: feedback ratings, evaluation scores, grounding/hallucination rates, escalation rates.
- Reliability: availability, time to first token, end-to-end latency, error rate against SLOs.
- Cost: cost per active user and per task, token efficiency, cache hit rate.
- Risk: policy violations blocked, incidents, data-leak near misses, audit findings.

Avoid vanity metrics; measure against baselines for specific use cases.

## Likely follow-ups

- How would you measure "time saved" credibly?
- Which three metrics go on the leadership dashboard?

---

[← B0020](../../behavioural_questions/0020_model_agnostic_platform_challenges/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0022 →](../../behavioural_questions/0022_agent_use_cases_for_corporate_functions/README.md)

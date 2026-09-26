# Q0400 · Pre-launch evaluation plan for a new assistant

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation strategy | Hard |

## Question

A Corporate Treasury assistant (RAG over policies plus a read-only tool for cash positions) is due to launch in eight weeks. Lay out the evaluation plan week by week.

## Answer

- Weeks 1–2: agree success criteria with Treasury and Risk (quality, safety, latency, cost targets). Collect and label about 300 real questions (stratified, including unanswerable and entitlement-sensitive ones) with SMEs, and write the annotation guidelines. Build deterministic tests and fakes for the tool and retrieval code.
- Weeks 3–4: baseline runs with component metrics (retrieval hit rate, context recall) and end-to-end metrics (correctness, groundedness, citation accuracy, abstention). Calibrate an LLM judge against SME labels. Error analysis, then fixes to chunking, retrieval and prompts. Add tool-call evaluations (correct tool, correct arguments, entitlement checks).
- Week 5: safety and security: red-team (injection through documents, data-extraction attempts, tool misuse), entitlement leak probes across personas, PII checks, over-refusal set. Fix findings and add them as regression cases.
- Week 6: performance and cost: load testing at the expected concurrency, TTFT and latency SLO checks, cost per query, fallback behaviour when a provider throttles.
- Week 7: pilot with 20–50 Treasury users, with feedback capture, sampled judge scoring, and daily error review. Model-risk validation pack prepared from the run manifests and results.
- Week 8: go/no-go against the criteria, with a canary rollout plan, dashboards and alerts live, runbooks and on-call owners set, and a post-launch review scheduled for two weeks later.

## Likely follow-ups

- What would make you delay the launch even if the average quality met the target?
- Which evaluations continue after launch, and at what cadence?

---

[← Q0399](../../batch_04_llm_evaluation_observability/0399_design_an_evaluation_platform_for_llm_suite/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md)

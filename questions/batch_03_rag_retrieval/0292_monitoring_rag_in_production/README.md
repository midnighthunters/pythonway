# Q0292 · Monitoring RAG in production

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Operations | Medium |

## Question

What would you monitor for a production RAG assistant, and which alerts would you set?

## Answer

Retrieval:
- Zero-result and low-confidence rates, the top-score distribution, the fraction of queries with identifiers, and drift in query topics.
- Index freshness (ingestion lag), ingestion failures and quarantine counts, and the ACL sync lag.

Generation:
- Abstention rate, citation presence and validity, sampled groundedness scores, answer length, and `finish_reason` distributions (truncation).
- Guardrail triggers (injection, PII), and refusal rates.

User signals: feedback rate and ratio, citation clicks, follow-up rephrasing (a sign of a bad answer), and escalations to humans.

System: latency per stage (p50, p95, p99), TTFT, token usage, cost per query, error rates and 429s per provider, and cache hit rates.

Alerts: a spike in zero results (index outage or a filter bug), ingestion lag above the SLO, a groundedness drop after a deployment, an ACL sync failure (security), and latency or error SLO burn.

Dashboards should be sliceable by assistant, business line, model, prompt and index version.

## Likely follow-ups

- Which of these alerts is a security incident rather than a quality issue?

---

[← Q0291](../../batch_03_rag_retrieval/0291_learn_from_user_feedback/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0293 →](../../batch_03_rag_retrieval/0293_interleaving_tests_for_retrievers/README.md)

# B0062 · Improving reliability of a system

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - operational stability | Medium |

## Question

Tell me about a time you significantly improved the reliability or operational stability of a system.

## Answer

- Situation: an internal RAG service at 97% availability with frequent timeouts at peak.
- Action: analysed incidents (slow vector queries, provider 429s, missing timeouts); added timeouts and jittered retries, a circuit breaker, per-dependency bulkheads, embedding caching, autoscaling on queue depth and provider fallback; defined SLOs, alerts and runbooks.
- Result: availability 97% → 99.9%, p95 latency down 40%, pages down 80%.

## Likely follow-ups

- How did you prioritise which fixes to do first?
- How did you verify the improvement was real?

---

[← B0061](../../behavioural_questions/0061_reducing_technical_debt_while_delivering/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0063 →](../../behavioural_questions/0063_making_a_significant_performance_improvement/README.md)

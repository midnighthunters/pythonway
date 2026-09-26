# B0069 · Your most challenging bug

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - debugging | Medium |

## Question

Tell me about the most challenging bug you have debugged.

## Answer

Structure: symptom → hypotheses → evidence → root cause → fix → prevention.

- Symptom: agents occasionally created the same ticket twice.
- Evidence: logs showed client retries after exactly 60 seconds.
- Root cause: the load balancer's idle timeout closed quiet streaming connections, the client retried the whole request, and the ticket tool was not idempotent.
- Fix: heartbeat events on the SSE stream, idempotency keys on tool calls, server-side dedupe, a safer client retry policy.
- Prevention: a fault-injection test for dropped connections and an alert on duplicate-key hits.

Highlight the method: reproduce, add instrumentation, test one hypothesis at a time.

## Likely follow-ups

- How did you reproduce it?
- Which tooling helped most?

---

[← B0068](../../behavioural_questions/0068_working_under_pressure/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0070 →](../../behavioural_questions/0070_going_above_and_beyond_for_a_user/README.md)

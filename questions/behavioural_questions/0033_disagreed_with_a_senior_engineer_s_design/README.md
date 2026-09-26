# B0033 · Disagreed with a senior engineer's design

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - collaboration | Medium |

## Question

Tell me about a time you disagreed with a senior engineer's design.

## Answer

- Situation: e.g. a lead proposed synchronous sequential calls from the chat API to five tools; you worried about latency and cascading failures.
- Action: did the homework first (measured p95 per tool, modelled the latency budget), raised it in the design review with data, proposed alternatives (parallel fan-out with per-tool timeouts, or an async job with streamed status) and acknowledged the strengths of their approach (simplicity).
- Result: a hybrid was agreed and p95 met target. Or, if you were overruled, you committed fully and added monitoring that later informed a revision.
- Show respect for experience and genuine openness to being wrong.

## Likely follow-ups

- What would you do if you were overruled but still believed you were right?
- How do you disagree in a written design doc?

---

[← B0032](../../behavioural_questions/0032_gave_difficult_feedback_to_a_peer/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0034 →](../../behavioural_questions/0034_worked_with_a_difficult_teammate/README.md)

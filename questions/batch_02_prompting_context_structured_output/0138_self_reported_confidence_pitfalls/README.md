# Q0138 · Self-reported confidence pitfalls

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Reliability | Medium |

## Question

Your schema has a `confidence: 0–1` field that the model fills in. Can you use it to auto-approve outputs?

## Answer

Not directly.
- Self-reported confidence is text the model generates, not a probability. It is often poorly calibrated and clusters at round numbers (0.9, 0.95).
- It can be insensitive to real errors. The model says 0.95 when it has misread the document.
- It shifts between model versions and prompt changes.

Better signals:
- Token logprobs of the answer (where available), agreement across several samples (self-consistency), and a separate verifier or judge.
- Rule checks: schema validity, cross-field arithmetic, entity spans that exist in the source, citations present.
- Calibrate whichever signal you use against labelled outcomes, and pick thresholds for a target precision.

Self-reported confidence can still be one feature in a calibrated router, but never the sole basis for automation in a regulated process.

## Likely follow-ups

- How would you build a calibrated auto-approve threshold for an extraction pipeline?

---

[← Q0137](../../batch_02_prompting_context_structured_output/0137_multi_label_classification_output/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0139 →](../../batch_02_prompting_context_structured_output/0139_verify_extracted_entities_against_the_source/README.md)

# Q0352 · Annotation guidelines and quality control

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Human evaluation | Medium |

## Question

What goes into good annotation guidelines for labelling LLM outputs, and how do you keep label quality high over time?

## Answer

Guidelines:
- A precise definition of each label or score with positive and negative examples, including tricky boundary cases.
- A decision procedure ("first check faithfulness against the sources, then completeness…").
- How to handle uncertainty ("unsure" or "needs expert" options instead of forced guesses).
- What evidence to record (quote the unsupported claim).
- Versioned, with a changelog, because label meaning must not drift silently.

Quality control:
- Calibration sessions before labelling starts, and practice rounds with feedback.
- Gold or honeypot items with known answers mixed in, tracking accuracy per annotator.
- An overlap subset for agreement (kappa), and adjudication by a senior reviewer.
- Periodic re-calibration, and monitoring for fatigue (time per item, sudden accuracy drops).
- Feeding disagreements back into guideline clarifications.

## Likely follow-ups

- How would you detect an annotator who is clicking through without reading?

---

[← Q0351](../../batch_04_llm_evaluation_observability/0351_designing_a_human_evaluation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0353 →](../../batch_04_llm_evaluation_observability/0353_offline_versus_online_evaluation/README.md)

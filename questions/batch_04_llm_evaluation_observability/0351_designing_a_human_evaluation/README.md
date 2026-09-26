# Q0351 · Designing a human evaluation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Human evaluation | Medium |

## Question

You need expert human evaluation of a new Legal drafting assistant. How do you design it?

## Answer

- Goal and decision: what will this evaluation decide (launch, choose between two versions, measure accuracy)? That drives the design.
- Sample: a stratified sample of realistic tasks (easy and hard, each document type), sized for the needed precision (at least 100–200 items for rate estimates).
- Format: absolute rubric ratings (each dimension on an anchored scale) for quality estimates, or blinded side-by-side preference for comparing versions (randomised order, hidden system identity).
- Raters: qualified SMEs, trained on guidelines with worked examples. Overlap 20–30% of items for inter-rater agreement.
- Tooling: an annotation interface showing the sources, capturing ratings, error categories and free-text comments, and time spent.
- Quality control: agreement statistics, gold items with known answers, and adjudication of disagreements.
- Analysis: confidence intervals, slices, an error taxonomy, and examples for stakeholders.
- Ethics and data handling: approved data, confidentiality of the drafts, and rater workload.

## Likely follow-ups

- When would you prefer side-by-side over absolute ratings?

---

[← Q0350](../../batch_04_llm_evaluation_observability/0350_slice_evaluation_results_by_segment/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0352 →](../../batch_04_llm_evaluation_observability/0352_annotation_guidelines_and_quality_control/README.md)

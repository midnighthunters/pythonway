# Q0331 · Evaluating summarisation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Summarisation evaluation | Medium |

## Question

How would you evaluate a meeting-notes or report summariser for an internal platform?

## Answer

Dimensions and methods:
- Faithfulness: no claims unsupported by the source. Claim decomposition plus an entailment judge, and number and entity checks against the source.
- Coverage: the key points a human expects. Have SMEs write 3–7 key points per document and check coverage with a judge or keywords.
- Conciseness and format: length limits, required sections (actions, owners, dates).
- Correct attribution: who said or decided what (a common error in meeting summaries).
- Usefulness: SME rubric ratings on a sample, or side-by-side preference against the current process.

Process: a diverse document set (short and long, messy transcripts, tables), metrics per document type, human review of a sample every release, and online feedback. Overlap metrics like ROUGE are tracking signals only.

## Likely follow-ups

- How would you catch a summary that attributes a decision to the wrong person?

---

[← Q0330](../../batch_04_llm_evaluation_observability/0330_field_level_extraction_evaluation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0332 →](../../batch_04_llm_evaluation_observability/0332_key_point_coverage_metric/README.md)

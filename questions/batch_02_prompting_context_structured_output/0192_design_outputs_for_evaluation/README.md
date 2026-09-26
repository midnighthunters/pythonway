# Q0192 · Design outputs for evaluation

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Evaluation-friendly design | Medium |

## Question

How do you design model outputs so they are easy to evaluate automatically?

## Answer

- Separate machine-checkable fields from prose: `label`, `status`, `citations`, `extracted_values` in structured form, with free text in its own field.
- Use closed sets (enums) wherever possible, so exact-match metrics work.
- Require evidence: citations, quote spans, and page references that can be verified against sources.
- Include explicit abstention or status values ("not_found", "needs_human"), so abstention can be measured.
- Keep formats stable across versions (versioned schemas), so the evaluation history stays comparable.
- Log inputs, retrieved context ids, model and prompt versions, tool calls and outputs with a trace id, so any production case can become an evaluation case.

This makes CI evaluation gates deterministic where possible, and focuses expensive LLM-as-judge or human review on the genuinely open-ended parts.

## Likely follow-ups

- Which parts of a policy Q&A answer can be scored without an LLM judge?

---

[← Q0191](../../batch_02_prompting_context_structured_output/0191_tell_the_model_about_tool_side_effects/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0193 →](../../batch_02_prompting_context_structured_output/0193_prompt_anti_patterns/README.md)

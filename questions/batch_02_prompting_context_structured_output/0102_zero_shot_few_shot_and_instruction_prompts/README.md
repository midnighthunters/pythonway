# Q0102 · Zero-shot, few-shot and instruction prompts

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Easy |

## Question

Compare zero-shot, few-shot and instruction-only prompting. When does each one fit?

## Answer

- Zero-shot with clear instructions: the default for capable instruction-tuned models on common tasks (summarise, classify into described labels, extract fields). It is the cheapest and easiest to maintain.
- Few-shot (2–5 examples): use it when the format, labelling conventions or edge-case handling are hard to describe but easy to show, such as a house style, tricky label boundaries or unusual output formats. Examples cost tokens every call and can bias outputs, so pick them deliberately.
- Detailed instructions plus a schema (structured outputs): use it when a machine consumes the output. The schema does more than examples can.

Rule of thumb: start zero-shot with precise instructions, measure on an evaluation set, then add targeted examples for the failure modes you see. Prefer dynamic example selection over static examples when inputs vary a lot.

## Likely follow-ups

- What is a sign that you've added too many few-shot examples?

---

[← Q0101](../../batch_02_prompting_context_structured_output/0101_anatomy_of_a_good_system_prompt/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0103 →](../../batch_02_prompting_context_structured_output/0103_render_versioned_prompt_templates_safely/README.md)

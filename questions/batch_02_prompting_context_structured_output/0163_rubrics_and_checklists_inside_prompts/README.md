# Q0163 · Rubrics and checklists inside prompts

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Easy |

## Question

How do checklists and rubrics in prompts improve outputs, for example for a code-review or document-review assistant?

## Answer

- They turn a vague goal ("review this") into explicit criteria the model must address: security (injection, secrets, authorisation), correctness, error handling, tests, naming, and performance.
- They improve coverage and consistency across runs and reviewers, and make the output structured (one section per criterion, "no issues found" where applicable).
- They support evaluation: the same rubric can drive an LLM-as-judge or human grading.

Tips: keep the list short and prioritised (5–8 items), define severity levels, ask for evidence (line numbers or quotes) for each finding, allow "not applicable", and put the output schema at the end. Too many criteria dilute attention, so split them into several focused passes if needed (a security pass, then a style pass).

## Likely follow-ups

- When would you split one rubric into multiple model calls?

---

[← Q0162](../../batch_02_prompting_context_structured_output/0162_system_prompt_confidentiality/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0164 →](../../batch_02_prompting_context_structured_output/0164_generate_critique_and_revise_loop/README.md)

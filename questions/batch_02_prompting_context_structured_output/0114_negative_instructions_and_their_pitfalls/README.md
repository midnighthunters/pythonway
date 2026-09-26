# Q0114 · Negative instructions and their pitfalls

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Easy |

## Question

Why are prompts full of "DON'T" rules often less effective, and how do you rewrite them?

## Answer

- Long lists of prohibitions dilute attention, can conflict with each other, and sometimes prime the unwanted behaviour by mentioning it ("don't mention competitor X").
- They also don't tell the model what to do instead, so it improvises.

Rewrite as positive, specific guidance with an alternative:
- "Don't give investment advice" → "If asked for investment recommendations, explain that you can't provide advice and point to the approved research portal."
- "Don't be verbose" → "Answer in at most 3 bullets."
- "Never make up numbers" → "Only state figures that appear in the sources, and cite them."

Keep hard constraints that must never fail (data access, actions) enforced in code, not only in the prompt.

## Likely follow-ups

- Which rules belong in code rather than the prompt?

---

[← Q0113](../../batch_02_prompting_context_structured_output/0113_controlling_output_length/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0115 →](../../batch_02_prompting_context_structured_output/0115_measure_prompt_robustness_to_paraphrase/README.md)

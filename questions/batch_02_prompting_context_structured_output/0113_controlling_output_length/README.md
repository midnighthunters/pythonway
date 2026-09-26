# Q0113 · Controlling output length

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt design | Easy |

## Question

How do you reliably control the length of model outputs?

## Answer

- Instructions in countable units work better than vague ones: "3 bullet points, each under 20 words" beats "be concise". Word counts are approximate, and structure (bullets, sections, fields) is more reliable.
- A `max_tokens` cap is a hard stop, not a style instruction. Hitting it truncates mid-sentence (`finish_reason: length`), so set it above the expected length and treat truncation as an error for structured outputs.
- Schemas with `maxLength` or `maxItems` constrain structured fields. Enforce them in validation too.
- Few-shot examples of the desired length.
- Post-processing: if a summary must fit a UI card, validate the length and re-ask or trim at sentence boundaries.

Reasoning models' visible output can be short while hidden reasoning is long, so budget `max_tokens` for both.

## Likely follow-ups

- Why is asking for "exactly 100 words" unreliable?

---

[← Q0112](../../batch_02_prompting_context_structured_output/0112_teach_the_model_to_say_i_don_t_know/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0114 →](../../batch_02_prompting_context_structured_output/0114_negative_instructions_and_their_pitfalls/README.md)

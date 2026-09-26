# Q0195 · Language control in multilingual replies

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Global users | Easy |

## Question

Users write in many languages, and the sources are mostly English. How do you control the reply language and keep quality?

## Answer

- Instruction: "Reply in the language of the user's latest message unless they ask otherwise. Keep policy names, product names and quoted text in their original language." Place it in the system prompt, and optionally restate it near the end.
- Detect the language in code (a fast classifier) and pass it explicitly ("User language: fr"). This is more reliable than asking the model to infer it, especially for short or mixed messages.
- Cross-lingual retrieval: multilingual embeddings or query translation, since the sources may be in English.
- Keep citations and quotes in the source language, optionally with a translation, so users can verify them.
- Numbers and dates: format for the user's locale in code, not by the model.
- Evaluate per language, including guardrails and refusal quality.

## Likely follow-ups

- What should happen when a user switches language mid-conversation?

---

[← Q0194](../../batch_02_prompting_context_structured_output/0194_review_this_prompt/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0196 →](../../batch_02_prompting_context_structured_output/0196_few_shot_examples_from_production_data/README.md)

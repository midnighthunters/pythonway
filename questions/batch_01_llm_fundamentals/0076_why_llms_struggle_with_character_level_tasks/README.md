# Q0076 · Why LLMs struggle with character-level tasks

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tokenization | Easy |

## Question

Why do LLMs miscount letters in a word, fail at reversing strings, or make arithmetic errors, and how should an application handle those needs?

## Answer

- The model sees tokens, not characters. "strawberry" may be two or three tokens, so the individual letters aren't directly visible. The model has to have memorised each token's spelling.
- Numbers are split inconsistently into chunks of digits, which makes place value and carrying hard. Long multiplication is a multi-step algorithm the model must simulate token by token.
- Sampling adds errors, and one wrong digit is fatal for exact tasks.

Application pattern: don't ask the model to do what code does better. Give it tools (a calculator, a code interpreter, SQL, string utilities) and have it call them. Validate numbers in outputs against source data, especially financial figures in summaries. Reasoning models do better but still aren't guaranteed.

## Likely follow-ups

- How would you guarantee that the numbers in a generated earnings summary match the source table?

---

[← Q0075](../../batch_01_llm_fundamentals/0075_instruction_hierarchy_and_roles/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0077 →](../../batch_01_llm_fundamentals/0077_sliding_window_attention_mask/README.md)

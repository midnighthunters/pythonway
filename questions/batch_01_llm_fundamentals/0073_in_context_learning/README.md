# Q0073 · In-context learning

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Prompting fundamentals | Easy |

## Question

What is in-context learning, and what are its practical limits compared with fine-tuning?

## Answer

- In-context learning (ICL) means the model adapts its behaviour to instructions and examples in the prompt without any weight updates. Few-shot examples teach format, labels, style and edge cases.
- Why it works (informally): pre-training on huge, varied text teaches the model to infer the task from context and continue the pattern.

Limits:
- Every example costs tokens on every call, although prompt caching helps.
- It is sensitive to example choice, order and label balance. Examples can bias outputs (majority-label and recency effects).
- The context window caps how much you can teach, and it can't reliably install new knowledge at scale.
- Behaviour can shift between model versions.

Rule of thumb: start with clear instructions plus 2–5 diverse, representative examples. Pick examples dynamically by similarity to the query when the task varies. Move to fine-tuning when the prompt gets huge, or when you need consistent behaviour at very high volume.

## Likely follow-ups

- How would you select few-shot examples dynamically for each request?

---

[← Q0072](../../batch_01_llm_fundamentals/0072_why_chain_of_thought_helps/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0074 →](../../batch_01_llm_fundamentals/0074_scaling_laws_in_practice/README.md)

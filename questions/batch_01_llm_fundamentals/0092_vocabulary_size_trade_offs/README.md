# Q0092 · Vocabulary size trade-offs

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tokenization | Medium |

## Question

What are the trade-offs of a larger tokenizer vocabulary (for example 32k versus 256k tokens)?

## Answer

Larger vocabulary:
- Pros: fewer tokens per text, which means lower cost and latency per character and more effective context. Better coverage of many languages, code and whitespace patterns.
- Cons: bigger embedding and output matrices (vocabulary × d_model parameters each), a more expensive softmax per step, more rare tokens that are under-trained ("glitch tokens"), and more memory.

Smaller vocabulary has the opposite profile: longer sequences but a leaner output layer.

Why practitioners care: token efficiency differs across providers and languages, which changes cost comparisons and context limits. The same "128k context" holds different amounts of text in different models. Always benchmark cost on your own corpus, not per-token list prices alone.

## Likely follow-ups

- What are "glitch tokens", and how did they arise?

---

[← Q0091](../../batch_01_llm_fundamentals/0091_benchmark_contamination/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0093 →](../../batch_01_llm_fundamentals/0093_memory_needed_to_fine_tune/README.md)

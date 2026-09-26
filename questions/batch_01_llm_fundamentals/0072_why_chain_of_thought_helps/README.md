# Q0072 · Why chain-of-thought helps

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Reasoning techniques | Medium |

## Question

Why does asking a model to reason step by step improve accuracy on some tasks, and when is it a bad idea in production?

## Answer

Why it helps:
- A transformer does a fixed amount of computation per generated token. Writing intermediate steps gives it more serial computation and a scratchpad, so it can condition later tokens on earlier partial results.
- It decomposes multi-step problems (arithmetic, logic, planning) into steps that are each easier.
- Reasoning models have this behaviour trained in with reinforcement learning, so explicit "think step by step" prompts matter less for them.

When it's a bad idea:
- Latency and cost: many more output tokens.
- Simple tasks (classification, lookup, extraction) gain little or nothing.
- Leakage: visible reasoning can expose system-prompt details or sensitive intermediate data. Keep it internal, or ask for structured final outputs only.
- Faithfulness: the written reasoning isn't guaranteed to be the real cause of the answer. Don't treat it as an audit explanation.

Production pattern: reason internally, return a structured answer with citations, and let the evaluation decide whether the extra tokens pay off.

## Likely follow-ups

- Is a model's stated reasoning a reliable explanation for a regulator?

---

[← Q0071](../../batch_01_llm_fundamentals/0071_self_consistency_majority_voting/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0073 →](../../batch_01_llm_fundamentals/0073_in_context_learning/README.md)

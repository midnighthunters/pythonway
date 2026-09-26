# Q0074 · Scaling laws in practice

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Foundations | Medium |

## Question

What do LLM scaling laws say, and how should they influence an application team's decisions?

## Answer

- Empirically, pre-training loss falls smoothly as a power law in model size, data and compute. Compute-optimal training balances parameters and tokens (Chinchilla: about 20 tokens per parameter), and modern models are often trained far longer to make inference cheaper.
- Capabilities on downstream tasks improve less smoothly. Some look like sudden jumps, partly an artefact of harsh metrics such as exact match.
- Test-time compute is another scaling axis: more reasoning tokens or more samples can buy accuracy.

For an application team:
- Expect newer and smaller models to keep getting better and cheaper, so design for model agility (abstraction layer, evaluations, quick swaps) rather than hard-coding one model.
- Spend engineering effort on data, retrieval, tools and evaluation, which don't depreciate when a new model ships.
- Re-check cost and quality trade-offs every few months, because the best model for a task changes.

## Likely follow-ups

- Why might a smaller model trained on more data beat a larger model for your use case?

---

[← Q0073](../../batch_01_llm_fundamentals/0073_in_context_learning/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0075 →](../../batch_01_llm_fundamentals/0075_instruction_hierarchy_and_roles/README.md)

# Q0048 · Fine-tune, RAG or prompt

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Solution design | Medium |

## Question

A business team wants the assistant to "know our internal policies and write in our house style". How do you decide between prompting, RAG and fine-tuning?

## Answer

Decide by the kind of gap:
- Knowledge (facts, policies, documents that change): use RAG. It is updatable without retraining, supports citations and entitlement filtering, and keeps an audit trail of the sources used.
- Behaviour or format (house style, output schema, classification labels, tool-use patterns): start with prompting and few-shot examples. If that is insufficient, costly (very long prompts) or inconsistent at scale, fine-tune with SFT or LoRA.
- Capability (a model that can't reason well enough): try a stronger or reasoning model, better decomposition or tools. Fine-tuning rarely adds deep new capabilities.

Decision process:
1. Build an evaluation set first, with success criteria.
2. Prompt baseline → RAG if knowledge is missing → fine-tune only if evaluations show a behaviour gap that prompting can't close.
3. Weigh the ongoing costs. Fine-tunes need data pipelines, re-training on base-model upgrades, model-risk validation and serving. RAG needs index maintenance.

Often the answer is a combination: RAG for policies, plus a small prompt or fine-tune for style.

## Likely follow-ups

- Why is fine-tuning a poor way to inject frequently changing facts?
- What evidence would convince you a fine-tune is worth its maintenance cost?

---

[← Q0047](../../batch_01_llm_fundamentals/0047_qlora_and_nf4_quantisation/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0049 →](../../batch_01_llm_fundamentals/0049_catastrophic_forgetting/README.md)

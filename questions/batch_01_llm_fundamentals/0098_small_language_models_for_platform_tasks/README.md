# Q0098 · Small language models for platform tasks

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Model selection | Medium |

## Question

Where do small language models (roughly 1–10B parameters) or classic ML fit on an enterprise GenAI platform?

## Answer

Good fits, where volume is high, the task is narrow and latency matters:
- Routing and intent classification (which agent or tool handles this?).
- Guardrails: prompt-injection and jailbreak classifiers, PII and NER detection, toxicity checks.
- Query rewriting, keyword extraction and metadata tagging for retrieval.
- Rerankers and embeddings.
- Summarising tool outputs before they go to a larger model.

Benefits: millisecond latency, low cost, self-hostable for data control, and they can be fine-tuned on labelled platform data.

Trade-offs: weaker reasoning and knowledge, so pair them with a fallback to a larger model. Operationally, someone owns their training, evaluation and serving.

Architecture: a gateway pipeline where cheap models handle pre-processing and control decisions, and large models do the generation.

## Likely follow-ups

- How would you collect training data for a routing classifier safely?

---

[← Q0097](../../batch_01_llm_fundamentals/0097_multilingual_performance_considerations/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0099 →](../../batch_01_llm_fundamentals/0099_continue_generation_past_the_output_limit/README.md)

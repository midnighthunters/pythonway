# Q0381 · End-to-end versus component RAG evaluation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | RAG evaluation | Medium |

## Question

Should you evaluate a RAG system end to end, or component by component?

## Answer

Both, for different purposes.
- End-to-end (question in, final answer scored for correctness, groundedness and citations) is what users experience and what gates releases. It can't tell you why something failed.
- Component metrics localise failures:
  - Ingestion: parse success rate, chunk quality checks.
  - Retrieval: hit rate@k, recall@k, nDCG on labelled relevance.
  - Reranking and packing: context precision, the fraction of needed facts in the final context (context recall).
  - Generation given perfect context: faithfulness and correctness when you feed the gold chunks. This isolates the model and prompt from retrieval.
- Diagnostic matrix: if generation with gold context is good but end-to-end is bad, fix retrieval. If both are bad, fix the prompt or model.

Keep component metrics cheap and frequent, and run end-to-end judged evaluations for releases.

## Likely follow-ups

- How do you evaluate generation "given perfect context" in practice?

---

[← Q0380](../../batch_04_llm_evaluation_observability/0380_evaluating_memory_and_personalisation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0382 →](../../batch_04_llm_evaluation_observability/0382_error_taxonomy_counts/README.md)

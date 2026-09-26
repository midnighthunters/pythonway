# Q0087 · Batch inference APIs for offline workloads

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Cost optimisation | Medium |

## Question

When should you use a provider's asynchronous batch API instead of real-time calls, and what changes in your design?

## Answer

Batch APIs, offered by OpenAI and Azure OpenAI and as batch inference on Bedrock, accept a file of requests and return results within a window (often up to 24 hours), typically at a meaningful discount and with separate, larger quotas.

Good fits: nightly document classification, backfilling summaries, evaluation runs, large extraction jobs, and re-embedding a corpus. Poor fits: anything interactive or time-sensitive.

Design changes:
- A job pipeline: prepare a JSONL of requests with stable custom ids, upload, poll or receive a notification, download the outputs and errors, then reconcile by id.
- Idempotency and partial failure: retry failed items, and don't redo succeeded ones.
- Data handling: batch input files are stored by the provider for a period, so check retention and data-classification rules.
- Monitoring: job SLAs, cost per job, and failure rates.

## Likely follow-ups

- How would you make a nightly batch job restartable after a crash halfway through reconciliation?

---

[← Q0086](../../batch_01_llm_fundamentals/0086_pack_texts_into_embedding_batches/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0088 →](../../batch_01_llm_fundamentals/0088_handling_a_stream_that_breaks_mid_response/README.md)

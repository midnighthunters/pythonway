# Q0296 · Streaming RAG answers with citations

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | UX engineering | Medium |

## Question

How do you stream a RAG answer token by token while still showing reliable citations and applying safety checks?

## Answer

- Send a sources event first: before generation starts, stream the list of candidate sources (titles and links) to the client, so citations `[n]` can be linked as they appear.
- Stream tokens as they arrive, and parse citation markers incrementally (buffer partial `[1` tokens). Link valid ids, and flag invalid ones.
- Safety: run input guardrails before generation. For output, run cheap incremental checks (PII patterns, markdown sanitisation) on buffered sentences, and heavier checks (groundedness, policy) when the answer completes. If a late check fails, replace or annotate the answer ("This answer was withdrawn") and log it.
- Send a final event with status (answered, abstained or blocked), the citations actually used, a trace id and usage, so the client knows the stream finished.
- Handle disconnects by cancelling upstream generation.

The trade-off is that streaming improves perceived latency, but post-hoc checks can only retract, not prevent. For high-risk assistants, buffer the full answer before display, or stream only after the first sentence passes checks.

## Likely follow-ups

- For which assistants would you disable streaming entirely?

---

[← Q0295](../../batch_03_rag_retrieval/0295_invalidate_cached_answers_on_document_change/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0297 →](../../batch_03_rag_retrieval/0297_end_to_end_mini_rag_pipeline/README.md)

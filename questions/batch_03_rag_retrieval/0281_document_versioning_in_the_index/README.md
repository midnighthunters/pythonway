# Q0281 · Document versioning in the index

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

Policies are revised regularly. How do you handle document versions in a RAG index so users get the current rule, but "what was the rule last year?" still works?

## Answer

- Store the version metadata on every chunk: `version`, `effective_from`, `effective_to` (null while current) and `status` (current, superseded, draft).
- Default retrieval filter: `status = current` (or effective now). Drafts are only for their authors or reviewers.
- Time-scoped questions: extract the date and filter to versions effective on that date.
- On update: index the new version, mark the old one superseded with `effective_to`, atomically per document. Don't just overwrite, if history matters for audit.
- Citations show the version and the effective date.
- Retention: keep superseded versions per records policy, possibly in a separate, colder index.
- Evaluation: include questions whose answers changed between versions to catch stale retrieval.

## Likely follow-ups

- How do you stop a superseded version from outranking the current one?

---

[← Q0280](../../batch_03_rag_retrieval/0280_collapse_near_identical_hits_across_documents/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0282 →](../../batch_03_rag_retrieval/0282_deletion_and_erasure_in_vector_stores/README.md)

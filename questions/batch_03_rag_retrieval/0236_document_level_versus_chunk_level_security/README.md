# Q0236 · Document-level versus chunk-level security

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Security | Medium |

## Question

Should access control be enforced at the document level or the chunk level? What are the pitfalls of each?

## Answer

- Document-level (every chunk inherits the document's ACL): simple and matches source systems such as SharePoint. The pitfall is documents with mixed sensitivity (a report with a restricted appendix), which get either over-shared or over-restricted.
- Chunk- or section-level: precise, but depends on reliable section labelling at ingestion, and there are more ACL entries to sync. Mistakes are harder to spot.

Practical approach:
- Default to document-level ACLs synced from the source of truth, re-synced frequently or event-driven.
- Split genuinely mixed documents at ingestion into separately permissioned sections where the source supports it (labelled sections, sensitivity labels).
- Store the ACL on every chunk (denormalised) so filtering is fast, and keep a mapping to re-propagate changes.
- Test with an entitlement evaluation suite, and audit which chunk ids reached each prompt.

## Likely follow-ups

- How quickly must ACL changes propagate to the index, and how would you prove it?

---

[← Q0235](../../batch_03_rag_retrieval/0235_information_barriers_in_rag/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0237 →](../../batch_03_rag_retrieval/0237_tenant_isolation_in_vector_stores/README.md)

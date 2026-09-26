# Q0216 · Metadata schema for chunks

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

What metadata would you store with each chunk in an enterprise RAG index, and what is each field used for?

## Answer

- Identity: `chunk_id`, `doc_id`, `version`, `ordinal`, `content_hash`, used for idempotent upserts, change detection and citations.
- Source: `source_system`, `url` or deep link, `title`, `section_path`, `page`, used for citations and UI links.
- Security: `acl_groups` or `allowed_principals`, `classification` (public, internal, confidential), `business_line`, and information-barrier tags. Used for filtering inside the search.
- Temporal: `effective_from`, `effective_to`, `last_modified`, `ingested_at`, used for freshness, versions and time-travel questions.
- Scope: `jurisdiction`, `language`, `doc_type` (policy, procedure, FAQ), `owner` or `department`. Used for self-query filters and authority boosting.
- Processing: `embedding_model`, `chunker_version`, `parser`, `quality_flags` (OCR confidence), used for migrations and debugging.

Index the filterable fields as proper typed filter fields (not just text), and keep the payload small. Large fields such as the full text may live in a separate document store.

## Likely follow-ups

- Which of these fields must never be editable by document authors?

---

[← Q0215](../../batch_03_rag_retrieval/0215_incremental_re_indexing_on_document_change/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0217 →](../../batch_03_rag_retrieval/0217_build_an_inverted_index/README.md)

# Q0283 · PII in indexed content

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Data governance | Medium |

## Question

The corpus contains HR cases and customer emails with personal data. How do you handle PII in a RAG index?

## Answer

- Data minimisation: index only what the use case needs. Exclude or separate high-risk sources (HR case files, health data) unless there is an approved purpose.
- Classification at ingestion: detect PII (names, account numbers, national ids, addresses) with detectors. Tag chunks with the categories found.
- Options per category: redact or pseudonymise before indexing (keep a secure mapping if re-identification is needed), restrict access with ACLs to the purpose-bound groups, or exclude.
- Embeddings are derived personal data. They can leak content through inversion or membership inference, so protect them like the source.
- Retention and erasure: support deletion by data subject across the index, caches and logs.
- Output controls: PII leak filters on responses, and logging with redaction.
- Governance: a DPIA for the use case, a lawful basis, records of processing, and approval from the privacy office.

## Likely follow-ups

- Why is redacting after retrieval (instead of before indexing) weaker?

---

[← Q0282](../../batch_03_rag_retrieval/0282_deletion_and_erasure_in_vector_stores/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0284 →](../../batch_03_rag_retrieval/0284_prompt_injection_through_retrieved_documents/README.md)

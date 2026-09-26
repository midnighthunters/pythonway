# Q0237 · Tenant isolation in vector stores

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Security | Medium |

## Question

LLM Suite serves many business lines and application teams. How do you isolate their RAG data in shared search infrastructure?

## Answer

Options, from weakest to strongest isolation:
1. A shared index with a tenant filter on every query: cheapest, but a single missing filter leaks data. Enforce the filter in a data-access layer that callers can't bypass, never in application code.
2. An index or collection per tenant within a shared cluster: clear boundaries and easy deletion or offboarding, with more operational objects.
3. A separate cluster or account per tenant (or per data classification): strongest isolation, per-tenant encryption keys and networking, and higher cost.

Also consider noisy neighbours (quotas per tenant), per-tenant encryption keys, per-tenant embedding and index versions, audit logs, and deletion guarantees. Most platforms use a mix: per-tenant indexes for most teams, and dedicated infrastructure for highly confidential data.

## Likely follow-ups

- How would you prove to an auditor that tenant A can never retrieve tenant B's data?

---

[← Q0236](../../batch_03_rag_retrieval/0236_document_level_versus_chunk_level_security/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0238 →](../../batch_03_rag_retrieval/0238_build_numbered_context_with_a_citation_map/README.md)

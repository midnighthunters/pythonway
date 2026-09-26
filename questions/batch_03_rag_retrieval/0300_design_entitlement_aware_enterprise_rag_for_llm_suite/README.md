# Q0300 · Design entitlement-aware enterprise RAG for LLM Suite

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | System design | Hard |

## Question

Design the RAG capability for LLM Suite: hundreds of thousands of employees, many source systems with their own permissions, strict information barriers, multiple jurisdictions and both Azure and AWS. Cover ingestion, security, retrieval, generation, evaluation and operations.

## Answer

Ingestion:
- Connectors per source (SharePoint, Confluence, policy portals, document management), event-driven or scheduled, publishing to a queue.
- A processing pipeline: parse (layout-aware), clean, classify (sensitivity, PII), scan for injection, structure-aware chunking with contextual headers, deterministic ids, embedding with caching. Write to the index atomically per document version.
- ACLs and barrier tags pulled from the sources and identity systems, with nested groups resolved and change events propagated within an SLO (for example 15 minutes).

Storage: hybrid search indexes partitioned by domain or tenant (per-tenant indexes for sensitive business lines), with filterable ACL, jurisdiction, version and date fields, in each cloud region as residency requires.

Query path:
1. Authenticate, resolve the entitlements and barrier side, rate limit.
2. Condense, extract filters, route (RAG, SQL, tools, or direct).
3. Hybrid retrieval with security trimming inside the search, then RRF, then a cross-encoder rerank, then a calibrated gate.
4. Context packing (diversity, versions resolved, a budget), then a grounded prompt through the LLM gateway (model routing across Azure OpenAI and Bedrock).
5. Validate citations and groundedness (sampled or cheap checks), sanitise, stream with source links, and apply the answer cache scoped by entitlements.

Evaluation: golden sets per assistant and language, including unanswerable and entitlement-leak cases. CI gates on retrieval (hit rate, nDCG) and answer metrics (groundedness, citation accuracy, abstention). Canary on index, prompt or model changes.

Operations: dashboards for freshness, ACL lag, zero results, groundedness, latency by stage and cost. Security alerts on ACL sync failure or leak-test failures. Deletion workflows across index, caches and logs. Audit logs of which chunks reached which user's prompt.

Platform API: a retrieval service with a stable contract (query, user context, filters) that returns chunks with citations, so application teams build assistants without touching indexes directly.

## Likely follow-ups

- How would you prove to Compliance that the system respects information barriers?
- What would you build first in a 3-month MVP?

---

[← Q0299](../../batch_03_rag_retrieval/0299_cost_model_for_a_rag_service/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md)

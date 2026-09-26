# Q0274 · Multilingual RAG

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Global users | Medium |

## Question

How do you design RAG for a multilingual workforce when most source documents are in English, with some local-language policies?

## Answer

- Retrieval: multilingual embedding models place queries and documents from different languages in one space. For BM25, use language-specific analysers per field, or translate the query into English and search both.
- Jurisdiction and language metadata: prefer the local-language version of a local policy (the French policy for France), and fall back to the global English one, clearly labelled.
- Generation: answer in the user's language, keep quotes and citations in the source language (optionally translated), and preserve the exact terms (legal names, policy titles).
- Evaluation: per-language golden sets, especially for retrieval recall and faithfulness of translated answers.
- Guardrails and PII detection must work in every supported language.
- Chunking: sentence splitting and tokenisation differ by language (CJK text has no spaces).

## Likely follow-ups

- What risk does translating the query before retrieval introduce?

---

[← Q0273](../../batch_03_rag_retrieval/0273_typo_tolerant_term_matching/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0275 →](../../batch_03_rag_retrieval/0275_exact_match_routing_for_identifiers/README.md)

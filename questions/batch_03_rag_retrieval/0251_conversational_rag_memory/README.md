# Q0251 · Conversational RAG memory

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Conversation | Medium |

## Question

How should a multi-turn RAG assistant handle follow-up questions, references to earlier answers and topic switches?

## Answer

- Condense each follow-up into a standalone query for retrieval, using the last few turns.
- Retrieve fresh evidence every turn. Don't rely on the model remembering earlier sources. Optionally keep the previous turn's top sources as candidates ("sticky" context) for follow-ups like "what about exceptions?".
- Keep the prompt history short: a rolling summary plus the last turns. Keep the citations in the history so "the policy you mentioned" can be resolved.
- Detect topic switches (low similarity to the previous turn's query or sources) and drop the sticky context.
- Re-check entitlements on every turn (group membership can change mid-session), and never reuse another user's context.
- UX: show which sources the current answer used, and let users pin or unpin a document for focused Q&A.

## Likely follow-ups

- When should a follow-up reuse the previous turn's sources instead of searching again?

---

[← Q0250](../../batch_03_rag_retrieval/0250_semantic_cache_keys_with_entitlements/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0252 →](../../batch_03_rag_retrieval/0252_agentic_rag/README.md)

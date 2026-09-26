# Q0290 · RAG over email and chat

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Domain RAG | Medium |

## Question

A personal assistant must answer questions over the user's email and chat. What's different from policy-document RAG?

## Answer

- Per-user scope: the index is strictly per user (or mailbox permissions via delegation), with no cross-user retrieval. Often it uses the source's own search API (for example Microsoft Graph) at query time instead of copying data into a central index.
- Threads: deduplicate quoted replies, reconstruct conversation threads, and keep the participants, dates and subjects as metadata.
- Time: recency and dates are central ("what did Priya send last week?"), so parse and filter by time.
- Noise: signatures, disclaimers and newsletters need filtering.
- Attachments: parse and link them to their message.
- Security: emails are untrusted input (external senders), so injection risk is high. Keep tools least-privilege and require confirmation for actions.
- Retention and compliance: journaling and records rules, legal holds, and regulated communications. Don't store copies beyond the permitted retention.

## Likely follow-ups

- Why might querying Microsoft Graph at request time be preferable to indexing mailboxes centrally?

---

[← Q0289](../../batch_03_rag_retrieval/0289_rag_over_code_repositories/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0291 →](../../batch_03_rag_retrieval/0291_learn_from_user_feedback/README.md)

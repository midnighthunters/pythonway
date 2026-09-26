# Q0158 · What to store in long-term memory

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Memory | Medium |

## Question

A personal assistant should remember users across sessions. What should it store, what should it never store, and how should users control it?

## Answer

Store (useful, low-risk, user-facing):
- Stable preferences: language, format, home office, working hours, preferred tools.
- Ongoing context: current projects, recurring tasks, open to-dos (with expiry).
- Facts the user explicitly asked it to remember.

Avoid or restrict:
- Sensitive personal data (health, special-category data) and credentials or secrets.
- Client-confidential or material non-public information outside its entitlement context.
- Inferred traits, or anything the user didn't expect to be retained.

Controls:
- Transparency: the user can view, edit and delete memories. Show "remembered: …" when saving.
- Scope: per user, never shared across users. Check entitlements when a memory is used, not just when it's written.
- Provenance and freshness: where each memory came from, when, and a TTL or re-confirmation for stale items.
- Retention policy aligned with records management and privacy law (GDPR rights of access and erasure).
- Guard against memory poisoning: don't auto-save instructions from documents or emails.

## Likely follow-ups

- How would you stop an injected email from writing a malicious "memory"?

---

[← Q0157](../../batch_02_prompting_context_structured_output/0157_instruction_drift_in_long_conversations/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0159 →](../../batch_02_prompting_context_structured_output/0159_extract_user_preferences_into_structured_memory/README.md)

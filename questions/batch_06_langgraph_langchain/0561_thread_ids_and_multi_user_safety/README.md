# Q0561 · Thread ids and multi-user safety

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Security | Medium |

## Question

How do you make LangGraph threads and stores safe in a multi-user service?

## Answer

- Server-side thread creation: generate random, unguessable thread ids (UUIDv4), record the owner (user and tenant) in your own table, and check ownership on every invoke, resume, `get_state` and history call. Never trust a client-supplied thread id alone.
- Resume authorisation: resuming an interrupt (approving a payment) is a privileged action. Check that the caller is the owner or an authorised approver, and log it.
- Store namespaces from identity: build them from the authenticated user id and tenant (`("memories", tenant, user)`) injected through the runtime context, never from model output.
- No shared mutable objects: don't keep per-user clients or tokens in module globals. Pass them through the context.
- Data lifecycle: deletion by user across checkpoints and stores, and retention policies.
- Testing: concurrent multi-user tests, and attempts to access another user's thread (which must fail with 403 or 404).

LangGraph Server and Platform offer authentication and authorisation hooks for exactly this.

## Likely follow-ups

- Should a missing thread and a thread owned by someone else return the same error?

---

[← Q0560](../../batch_06_langgraph_langchain/0560_what_gets_serialised_in_checkpoints/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0562 →](../../batch_06_langgraph_langchain/0562_deploying_langgraph_applications/README.md)

# Q0496 · Cross-user isolation in shared agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Security | Medium |

## Question

One agent deployment serves thousands of users concurrently. What can leak between users, and how do you prevent it?

## Answer

Leak paths:
- Shared mutable state in the process: module-level caches, global variables, a reused conversation object, or a tool client holding the last user's token.
- Caches (semantic caches, tool-result caches) keyed without the user or entitlement scope.
- Memory stores and checkpoints with wrong namespace keys (the thread id reused, or guessable).
- Logs and traces visible across teams, and evaluation datasets built from production.
- Model context: previous users' data in few-shot examples, or long-lived sessions reused across users.

Prevention:
- A per-request context object (identity, tokens, tenant), passed explicitly or through contextvars, never globals.
- Unguessable thread ids, bound to the owner and checked on every access.
- Cache keys that include the user or entitlement scope, and no caching of personalised answers.
- Namespaced stores (LangGraph Store namespaces per user), with access checks in the data layer.
- Tests: concurrent multi-user integration tests asserting no cross-contamination, and fuzzing thread ids.

## Likely follow-ups

- How would you test for a cross-user leak under concurrency?

---

[← Q0495](../../batch_05_agentic_patterns_orchestration/0495_backpressure_in_agent_pipelines/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0497 →](../../batch_05_agentic_patterns_orchestration/0497_explain_what_the_agent_did/README.md)

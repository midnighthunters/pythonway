# B0094 · Your approach to code reviews

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Engineering practice | Medium |

## Question

How do you approach code reviews, as a reviewer and as an author?

## Answer

As reviewer:

- Correctness first (logic, edge cases, error handling, concurrency), then security (injection, secrets, authorisation, input validation, PII in logs), then design and maintainability, tests and performance. Leave style to linters.
- Be specific and kind, explain why, separate blocking issues from nits, and review promptly.

As author:

- Small, focused PRs with context (what, why, how it was tested), a self-review first, linked tickets, and open responses to feedback.

JPMorganChase loops often include a code-review exercise, so practise saying your checklist out loud: bugs, security (hard-coded credentials), naming, tests, logging, resource handling.

## Likely follow-ups

- What do you look at first in a PR?
- How do you handle a reviewer who blocks on style preferences?

---

[← B0093](../../behavioural_questions/0093_handling_scope_creep/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0095 →](../../behavioural_questions/0095_production_ready_for_an_agentic_capability/README.md)

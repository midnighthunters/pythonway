# Q0411 · Reflection and self-correction for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent patterns | Medium |

## Question

What is reflection in agents, and when does it help versus waste tokens?

## Answer

Reflection means the agent (or a separate critic) reviews its intermediate or final output against the goal and feedback, then revises it: "the tests still fail with X, so the fix is incomplete"; "the answer lacks citations for claim 2".

It helps when there is a real feedback signal: failing tests, validator errors, tool errors, a critic with a concrete rubric, or verification against sources. Code-fix agents (run the tests, reflect, patch again) are the classic success. Research tasks benefit from "what's still missing?" checks.

It wastes tokens when the model just re-reads its own output with no new information. Self-critique without grounding often rubber-stamps or makes arbitrary edits, and it can talk itself out of correct answers.

Implement it with bounded rounds, specific critique criteria, external signals wherever possible, and a record of what changed each round (for evaluation and audit).

## Likely follow-ups

- Why does reflection work so well for code with unit tests?

---

[← Q0410](../../batch_05_agentic_patterns_orchestration/0410_re_planning_after_a_failed_step/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0412 →](../../batch_05_agentic_patterns_orchestration/0412_router_pattern/README.md)

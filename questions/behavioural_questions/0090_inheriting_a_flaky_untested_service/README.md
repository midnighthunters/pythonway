# B0090 · Inheriting a flaky untested service

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Scenario | Medium |

## Question

You inherit a critical service that is flaky and has almost no tests. What do you do?

## Answer

- Stabilise first: add observability (logs, metrics, traces), find the top failure modes from past incidents, and take quick wins (timeouts, retries, resource limits).
- Build a safety net: characterisation tests that pin current behaviour where you will make changes, contract tests for the APIs, and a CI pipeline with linting and type checks.
- Improve incrementally: refactor behind the tests (strangler approach) and fix root causes in order of impact.
- Document: runbooks, architecture notes, ownership.
- Share a plan and progress metrics: incident count, MTTR, test coverage on critical paths.

Avoid a big-bang rewrite.

## Likely follow-ups

- When would you consider a rewrite?
- What are characterisation tests?

---

[← B0089](../../behavioural_questions/0089_primary_model_endpoint_failing/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0091 →](../../behavioural_questions/0091_two_teams_want_conflicting_platform_changes/README.md)

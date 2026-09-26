# Q0475 · Agentic code-fix loop design

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent design | Medium |

## Question

Design an agent that automatically proposes fixes for red CI builds using MCP servers for repository, CI and issue-tracker access.

## Answer

1. Trigger: a CI failure webhook arrives on a queue. Deduplicate by commit and job.
2. Gather context through MCP tools: failing job logs (truncated to the relevant errors), the diff of the triggering commit, the relevant source files (search and read tools), test files, and recent similar failures.
3. Diagnose: classify the failure (a test regression, a flaky test, a dependency or infrastructure issue, a lint or type error). Skip or route infrastructure and flaky issues, since not every red build is a code bug.
4. Fix loop: in a sandbox checkout, the agent proposes a patch, runs the targeted tests, reads the failures, and revises, with an iteration cap and a no-progress detector.
5. Output: open a pull request with the patch, an explanation, and the test evidence. It never pushes to protected branches. A human reviews and merges.
6. Safety: sandboxed execution (no secrets, restricted network), repository permissions scoped to branch creation, dependency and secret scanning on the patch, and no changes to CI configuration or security-sensitive files without escalation.

Metrics: the fraction of red builds with an accepted fix (for example 62% self-patched), MTTR (for example from 4 hours to 11 minutes), the reviewer acceptance rate, reverts, and cost per fix.

## Likely follow-ups

- Which file types or directories would you forbid the agent from modifying?

---

[← Q0474](../../batch_05_agentic_patterns_orchestration/0474_route_exceptions_to_remediation_playbooks/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0476 →](../../batch_05_agentic_patterns_orchestration/0476_code_fix_loop_with_test_feedback/README.md)

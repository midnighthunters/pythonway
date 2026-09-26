# Q0486 · Testing strategy for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Testing | Medium |

## Question

Describe a layered testing strategy for a tool-using agent.

## Answer

1. Unit tests: each tool (validation, authorisation, business rules, error mapping), parsers, policy rules, and state reducers. Fast and deterministic.
2. Control-flow tests with a scripted fake LLM: routing, loops, retries, approvals, stop conditions, error recovery and checkpoint and resume. They assert the trajectory and the state, not the wording.
3. Integration tests against simulated backends (fake airline, fake ledger) with fixtures: agent plus real prompts plus a real model on a small scenario set, asserting final-state checks.
4. Evaluation suites: larger scenario sets with task success, trajectory checks, safety and red-team cases, and pass^k reliability over repeated runs. These run in CI on prompt, model or tool changes.
5. Chaos and fault injection: tool timeouts, 429s and malformed responses. The agent must degrade gracefully.
6. Shadow and canary runs in production with monitoring.

Design for testability: inject the model client, tools and clock, keep side effects behind interfaces, and make every run replayable from its trace.

## Likely follow-ups

- Which layer catches prompt regressions, and which catches code regressions?

---

[← Q0485](../../batch_05_agentic_patterns_orchestration/0485_load_tools_on_demand/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0487 →](../../batch_05_agentic_patterns_orchestration/0487_simulated_backends_for_agent_tests/README.md)

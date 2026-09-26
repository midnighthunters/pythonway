# Q0483 · Judging the quality of a task decomposition

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Planning | Medium |

## Question

How do you tell whether an agent's plan or decomposition is good before executing it?

## Answer

Checks:
- Coverage: every requirement in the goal maps to at least one step (for example the hotel update isn't forgotten).
- Feasibility: every step uses an available tool, with obtainable inputs. Dependencies are acyclic, and no step depends on information that only a later step produces.
- Minimality: no redundant or irrelevant steps (a drift signal).
- Safety: side-effecting steps come after verification steps, the irreversible ones are last, and approvals are placed before commits.
- Granularity: steps that are small enough to verify, but not so tiny that every call becomes a plan step.
- Efficiency: independent steps marked parallelisable, and expensive steps justified.

Methods: deterministic validation (schema, tools exist, DAG check), rubric-based judging of coverage and ordering, and comparison with reference plans for common tasks. Show plans to users for approval on high-stakes tasks.

## Likely follow-ups

- How would you automatically check that a plan covers all parts of the request?

---

[← Q0482](../../batch_05_agentic_patterns_orchestration/0482_detect_goal_drift_during_a_run/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0484 →](../../batch_05_agentic_patterns_orchestration/0484_tool_selection_at_scale/README.md)

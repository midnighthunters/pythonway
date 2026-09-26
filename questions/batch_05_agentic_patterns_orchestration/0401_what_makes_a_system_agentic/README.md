# Q0401 · What makes a system agentic

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent foundations | Easy |

## Question

What distinguishes an "agent" from a chatbot or a fixed LLM pipeline?

## Answer

An agent uses an LLM to decide its own control flow: which actions (tools) to take, in what order, and when it is done, based on the observations it gets back. The key ingredients:
- A goal or task, rather than a single question.
- Tools that let it observe and act (search, APIs, code execution, other agents).
- A loop: think → act → observe → repeat, until a stop condition.
- State and memory across steps (and sometimes across sessions).
- Autonomy bounded by guardrails: budgets, permissions and human approvals.

A chatbot answers from its context. A fixed pipeline (retrieve → generate) has hard-coded steps. An agent chooses the steps. That flexibility is its power (open-ended tasks) and its risk (loops, wrong actions, cost, security).

## Likely follow-ups

- Is a RAG system with query rewriting an agent?

---

[← Q0400](../../batch_04_llm_evaluation_observability/0400_pre_launch_evaluation_plan_for_a_new_assistant/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0402 →](../../batch_05_agentic_patterns_orchestration/0402_workflows_versus_agents/README.md)

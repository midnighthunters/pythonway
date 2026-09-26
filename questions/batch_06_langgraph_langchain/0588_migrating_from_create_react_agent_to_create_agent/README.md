# Q0588 · Migrating from create_react_agent to create_agent

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Migration | Medium |

## Question

A codebase uses `langgraph.prebuilt.create_react_agent`. What changes when moving to LangChain 1.x `create_agent`, and how do you migrate safely?

## Answer

What changes:
- The import moves to `from langchain.agents import create_agent`. It is the recommended prebuilt agent going forward, built on LangGraph.
- Customisation moves to middleware: behaviours that used to need pre- and post-model hooks or custom prompts callables (dynamic prompts, summarisation, human-in-the-loop, tool retries, model fallback) become middleware.
- System prompts are passed as `system_prompt`, and structured final responses are configured through the response-format options.
- The result is still a compiled graph, so checkpointers, streaming, interrupts and subgraph use carry over.

Migration steps:
1. Pin the current behaviour with tests: trajectory and final-answer evaluations with fake models, plus a small real-model evaluation.
2. Port feature by feature (prompt, tools, hooks, then middleware), keeping thread and state compatibility in mind (the message state shape).
3. Run both versions side by side on the evaluation suite and in shadow mode.
4. Canary and remove the old code.

Check the official migration guide for the exact parameter mappings, since these APIs evolve.

## Likely follow-ups

- Which old hook would become which middleware in your agent?

---

[← Q0587](../../batch_06_langgraph_langchain/0587_exposing_a_langgraph_agent_over_a2a/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0589 →](../../batch_06_langgraph_langchain/0589_migrating_from_langchain_0_x_to_1_x/README.md)

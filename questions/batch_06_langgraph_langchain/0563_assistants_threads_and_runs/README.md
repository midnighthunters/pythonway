# Q0563 · Assistants, threads and runs

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph Server | Medium |

## Question

Explain the LangGraph Server resource model (assistants, threads, runs) and how a front end uses it.

## Answer

- Assistant: a deployed graph plus a specific configuration (model, prompts, tools, parameters). One graph can back many assistants (for example "policy Q&A for HR" and "policy Q&A for Treasury" with different configurations), and assistants can be versioned.
- Thread: a persistent conversation or workflow instance holding its checkpointed state across runs (multi-turn chat, a paused approval).
- Run: one execution of an assistant on a thread (or stateless) with some input. It can be streamed, waited on, or run in the background, and it has a status (pending, running, success, error, interrupted).

Front-end flow: create a thread, start a streaming run with the user's message, render the streamed tokens and events, and on an interrupt show the approval UI, then start a new run with `Command(resume=...)`. The thread's state endpoint restores the conversation on page reload. Other resources include the Store (long-term memory), cron jobs and webhooks.

## Likely follow-ups

- Why separate "assistant" from "graph"?

---

[← Q0562](../../batch_06_langgraph_langchain/0562_deploying_langgraph_applications/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0564 →](../../batch_06_langgraph_langchain/0564_double_texting_strategies/README.md)

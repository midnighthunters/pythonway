# Q0564 · Double-texting strategies

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph Server | Medium |

## Question

A user sends a second message while the agent is still processing the first. What are the double-texting strategies, and which would you choose for a banking assistant?

## Answer

Strategies (as in LangGraph Platform):
- Reject: refuse the new run while one is in progress. Simple and safe, but frustrating.
- Enqueue: queue the new message and run it after the current run completes. It preserves order.
- Interrupt: stop the current run (keeping its progress so far) and start a new one with the new message included.
- Rollback: cancel the current run, discard its progress, and start fresh with the new message.

Choice: for chat Q&A, interrupt or rollback feels natural ("actually, I meant Paris"). For agents mid-way through side effects (booking, payment), avoid rollback and interrupt: an in-flight tool call may already have executed. Prefer enqueue (or reject with a clear "still working on your previous request" message), and design side effects to be idempotent and checkpointed. The strategy can differ per assistant.

## Likely follow-ups

- Why is rollback dangerous for an agent that has already called a payment API?

---

[← Q0563](../../batch_06_langgraph_langchain/0563_assistants_threads_and_runs/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0565 →](../../batch_06_langgraph_langchain/0565_background_runs_and_webhooks/README.md)

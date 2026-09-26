# Q0567 · Streaming agents to a web front end

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | UX engineering | Medium |

## Question

Describe how to stream a LangGraph agent's output to a React front end, including tokens, tool status and interrupts.

## Answer

Server:
- Run the graph with `stream_mode=["messages", "updates", "custom"]`, and translate the chunks into typed SSE events: `token` (from the final-answer node only), `status` (node updates mapped to user-safe labels), `tool` (start and end summaries), `interrupt` (the approval request payload), and `done` (final status, citations, trace id) or `error`.
- Send a heartbeat to keep proxies from closing idle connections, and handle client disconnects by cancelling the run, or letting it continue in the background, depending on the use case.

Client:
- Use `EventSource` or `fetch` with a stream reader (or the LangGraph SDK's React `useStream` hook, which manages threads, messages, interrupts and reconnection), append tokens to the current message, show status chips, and render approval UIs on interrupt events with approve and reject buttons that start a resume run.
- On reload, fetch the thread state to restore the conversation and any pending interrupt.

Security: authenticate the stream, never send raw internal state, and sanitise the model markdown before rendering.

## Likely follow-ups

- What should happen to the run if the user closes the tab?

---

[← Q0566](../../batch_06_langgraph_langchain/0566_cron_jobs_for_agents/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0568 →](../../batch_06_langgraph_langchain/0568_observability_for_langgraph_with_langsmith/README.md)

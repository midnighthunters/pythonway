# Q0568 · Observability for LangGraph with LangSmith

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Observability | Medium |

## Question

How do you get useful traces for LangGraph agents, and what do you look for when debugging a bad run?

## Answer

Setup: enable LangSmith tracing (API key and project environment variables, and optionally a self-hosted or data-residency deployment), or export OpenTelemetry. Every graph run becomes a trace, with a span per node, each LLM call (prompt, output, tokens, latency) and each tool call. Add metadata and tags (assistant version, tenant, user pseudonym, thread id) through the config, so you can filter.

What to look for:
- The node sequence against the expected trajectory (did it skip the risk check, or loop?).
- The exact messages sent to the model at the failing step (was the context wrong, truncated or poisoned?).
- Tool calls and their arguments and results (a wrong argument, an error, a slow dependency).
- Token and latency breakdown per step (which node blew the budget).
- State at each checkpoint (combine with `get_state_history` for time travel).

Hygiene: mask personal data and secrets before sending traces (input and output masking hooks), sample traffic appropriately, restrict project access, and link each trace id to the application logs and user-facing error messages.

## Likely follow-ups

- Which fields would you mask before traces leave your network?

---

[← Q0567](../../batch_06_langgraph_langchain/0567_streaming_agents_to_a_web_front_end/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0569 →](../../batch_06_langgraph_langchain/0569_async_nodes_and_ainvoke/README.md)

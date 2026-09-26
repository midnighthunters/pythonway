# Q0572 · Error handling strategy in LangGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Reliability | Medium |

## Question

Describe a layered error-handling strategy for a LangGraph agent in production.

## Answer

- Inside tools: validate the arguments, map exceptions to model-facing error messages (retryable or not, with a hint), and never leak internals.
- `ToolNode(handle_tool_errors=...)`: tool failures become error `ToolMessage`s, so the model can recover, rather than crashing the run.
- Node retry policies: retry transient infrastructure errors (timeouts, 429s, 503s) with backoff, and restrict retries to specific exception types.
- Model resilience: `with_fallbacks` to alternate models or deployments, timeouts on model calls, and circuit breakers at the gateway.
- Graph-level routing: nodes set error or degraded flags in the state, and conditional edges route to recovery, re-planning, human escalation, or a graceful final answer.
- Run-level: recursion and step limits, budgets, and a top-level exception handler in the serving layer that marks the run as failed, notifies the user with a trace id, and keeps the checkpoint for debugging or resume.
- Side effects: idempotency keys and compensations, so retries and resumes are safe.

Emit metrics per error class, and alert on spikes.

## Likely follow-ups

- Which errors should stop the run immediately rather than be retried?

---

[← Q0571](../../batch_06_langgraph_langchain/0571_timeouts_inside_nodes/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0573 →](../../batch_06_langgraph_langchain/0573_model_fallbacks_with_with_fallbacks/README.md)

# Q0519 · Agent middleware in LangChain 1.x

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain agents | Medium |

## Question

What is middleware in LangChain 1.x agents, and what kinds of cross-cutting concerns does it handle?

## Answer

Middleware hooks into the agent loop around model and tool calls, without rewriting the loop. Hooks exist at points such as before and after the model call, wrapping the model call, and wrapping tool calls, and middleware can also modify the request (messages, tools, model) dynamically.

Typical uses:
- Human-in-the-loop: pause before specific tool calls for approve, edit or reject decisions (built in).
- Summarisation: compress long histories when they exceed a token threshold (built in).
- PII handling: detect and redact or mask sensitive data in inputs and outputs.
- Dynamic behaviour: choose the model per request (cheap versus strong), filter the tool list by user role, or change the system prompt by context.
- Reliability: model fallbacks, retries, call limits (cap model or tool calls per run).
- Guardrails and logging: policy checks on tool calls, audit logs, metrics.

Guidance: compose small single-purpose middleware, order them deliberately (for example redaction before logging), test each one with fake models, and keep security-critical checks in the tools and platform as well, since middleware is a convenience layer, not the only control.

## Likely follow-ups

- In what order would you put PII redaction, logging and human-in-the-loop middleware?

---

[← Q0518](../../batch_06_langgraph_langchain/0518_create_agent_in_langchain_1_x/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0520 →](../../batch_06_langgraph_langchain/0520_human_in_the_loop_middleware/README.md)

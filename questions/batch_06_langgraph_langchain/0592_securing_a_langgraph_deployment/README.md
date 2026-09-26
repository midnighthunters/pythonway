# Q0592 · Securing a LangGraph deployment

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Security | Hard |

## Question

What security controls does a production LangGraph service need?

## Answer

- Authentication and authorisation at the API: validate user tokens, map them to tenants, check thread ownership on every call, and authorise resumes (approvals) separately. LangGraph Server offers custom auth handlers for this.
- Tool security: least-privilege tools per assistant, per-call authorisation using on-behalf-of credentials, argument validation, approval gates for side effects, rate limits and audit logs.
- Prompt-injection resilience: treat retrieved documents, emails and tool outputs as untrusted. Isolate untrusted content from tool authority, and monitor for drift and exfiltration patterns.
- Data protection: encrypt checkpoints and stores, keep secrets out of the state (use the runtime context and a secrets manager), set retention and deletion policies, and mask traces.
- Network: private endpoints to the LLM gateway, MCP servers and databases, and egress allowlists for tools that browse or call external APIs.
- Supply chain: pinned and scanned dependencies (LangChain, integrations, MCP adapters), and reviewed community packages.
- Runtime limits: recursion limits, budgets, timeouts and max concurrency per tenant, to contain abuse and runaway costs.
- Monitoring: alerts on unusual tool usage, authorisation failures, guardrail triggers and cost spikes, plus kill switches per assistant.

## Likely follow-ups

- How would you stop one tenant's runaway agent from exhausting shared workers?

---

[← Q0591](../../batch_06_langgraph_langchain/0591_performance_tuning_for_langgraph_apps/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0593 →](../../batch_06_langgraph_langchain/0593_debugging_a_stuck_or_looping_graph/README.md)

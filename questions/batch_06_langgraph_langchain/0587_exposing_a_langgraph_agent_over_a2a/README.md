# Q0587 · Exposing a LangGraph agent over A2A

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | A2A integration | Medium |

## Question

Another team wants to delegate tasks to your LangGraph agent from their own agent framework. How would you expose it via the A2A protocol?

## Answer

- Publish an Agent Card (at the well-known path, and in the platform registry) describing the agent: name, description, skills with example prompts, supported interfaces (URL, protocol binding and version), capabilities (streaming, push notifications), and security schemes (OAuth2 or mTLS). Sign it (A2A v1.0 supports JWS signatures).
- Map A2A to LangGraph: an A2A `SendMessage` becomes a run on a thread keyed by the A2A `contextId`, and the A2A task id maps to your run id. Your graph's lifecycle maps to task states: working while running, input-required on an `interrupt()`, then completed or failed, or canceled on cancel. Results become artifacts (text or data parts).
- Streaming: `SendStreamingMessage` or `SubscribeToTask` forwards your graph's stream as status and artifact update events. Long tasks can use push notifications instead.
- Security: authenticate the calling agent (and the end user it acts for), authorise per skill, enforce tenancy, and treat incoming messages as untrusted input.
- Operations: version the Agent Card and skills, apply rate limits and quotas per caller, and propagate traces.

## Likely follow-ups

- How would an `interrupt()` in your graph surface to the calling agent over A2A?

---

[← Q0586](../../batch_06_langgraph_langchain/0586_using_mcp_tools_in_langgraph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0588 →](../../batch_06_langgraph_langchain/0588_migrating_from_create_react_agent_to_create_agent/README.md)

# Q0586 · Using MCP tools in LangGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | MCP integration | Medium |

## Question

How would you connect a LangGraph agent to tools hosted on MCP servers, and what production concerns come with it?

## Answer

- Use an MCP client adapter (for example `langchain-mcp-adapters`) that connects to one or more MCP servers, lists their tools, and converts them into LangChain tools, which you pass to `create_agent` or a `ToolNode`.
- Transport: Streamable HTTP for remote servers (the stdio transport is for local tools). Under the 2026-07-28 MCP revision, each request carries the protocol version and capabilities in `_meta`, with no session handshake, which fits stateless agent workers.

Production concerns:
- Authorisation: per-request OAuth tokens scoped to the user (on-behalf-of), resource indicators, and the server validating the audience. Never share one god-token across users.
- Tool curation: only allow approved servers and tools per assistant (an MCP gateway or registry). Filter the tool lists, and pin tool versions and schemas.
- Safety: treat tool results as untrusted content (injection), require approval for destructive tools (use MCP tool annotations as hints, and enforce in your code), and apply rate limits.
- Reliability and observability: timeouts, retries, trace-context propagation into MCP calls (`traceparent` in `_meta`), and caching list results per the cache hints.

## Likely follow-ups

- Why shouldn't you rely on an MCP server's `destructiveHint` annotation for safety decisions?

---

[← Q0585](../../batch_06_langgraph_langchain/0585_provider_agnostic_model_initialisation/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0587 →](../../batch_06_langgraph_langchain/0587_exposing_a_langgraph_agent_over_a2a/README.md)

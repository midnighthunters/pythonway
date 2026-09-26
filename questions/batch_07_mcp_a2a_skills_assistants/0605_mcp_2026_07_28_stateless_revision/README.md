# Q0605 · MCP 2026-07-28 stateless revision

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

Explain the changes introduced in the MCP 2026-07-28 protocol revision regarding stateless operation and connection lifecycle.

## Answer

The MCP 2026-07-28 specification revision refined the transport and connection lifecycle to better support serverless, distributed, and multi-tenant cloud deployments:

Key changes:
1. Stateless Session Handling:
   - Early MCP drafts assumed a persistent stateful process per client connection. The 2026-07-28 revision allows servers to operate statelessly over HTTP by attaching session identifiers or authorization context to request headers (e.g. `Mcp-Session-Id` or JWT bearer tokens).
   - This enables deploying MCP servers as autoscaling container services behind load balancers (such as Azure Container Apps or AWS ECS) where successive tool calls may hit different worker instances.
2. Standardized Re-initialization & Capability Caching:
   - Clients can cache negotiated capabilities keyed by server version and session token, avoiding redundant `initialize` round-trips for every short-lived HTTP request.
3. Streamlined Streamable HTTP Transport:
   - Replaced fragile multi-endpoint SSE configurations with a cleaner single-endpoint HTTP POST stream for requests, responses, and streamed chunks.
4. Explicit Resource Expiration:
   - Resource representations can return `expiresAt` timestamps or ETags to allow client-side caching of heavy payloads (e.g. large compliance policy documents).

## Likely follow-ups

- How does stateless MCP handle `resources/subscribe` if the server cannot maintain long-lived in-memory client lists?
- What are the security benefits of ephemeral session tokens in stateless MCP?

---

[← Q0604](../../batch_07_mcp_a2a_skills_assistants/0604_mcp_transports_stdio_versus_sse_versus_streamable_http/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0606 →](../../batch_07_mcp_a2a_skills_assistants/0606_mcp_initialize_lifecycle_and_handshake/README.md)

# Q0604 · MCP transports: Stdio versus SSE versus Streamable HTTP

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

Compare the standard MCP transports: stdio, Server-Sent Events (SSE), and the Streamable HTTP transport introduced in recent revisions. When should an enterprise bank use each?

## Answer

MCP supports multiple transport mechanisms depending on isolation requirements and network boundaries:

1. Standard Input/Output (stdio):
   - Mechanism: The client spawns the server as a local child sub-process; messages are newline-delimited JSON strings over `stdin` and `stdout`. `stderr` is reserved for out-of-band logging.
   - Pros: Zero network overhead, local process isolation, inherently private to the host operating system user, no open ports or TLS certificates needed.
   - Cons: Local only. Cannot be shared across multiple machines or pooled as an enterprise microservice.
   - Bank Use Case: Developer tooling, secure local developer assistants, or sandbox CLI runners.

2. Server-Sent Events (SSE) over HTTP:
   - Mechanism: The client opens an HTTP GET connection to an `/sse` endpoint to receive server-to-client events. Client-to-server messages are sent via separate HTTP POST requests.
   - Pros: Works across networks, traverses corporate proxies and firewalls easily, enables remote microservices.
   - Cons: Asymmetric; stateful connection management; reconnect logic can lose in-flight messages unless message IDs are tracked.
   - Bank Use Case: Centralized enterprise services deployed in internal Kubernetes clusters (e.g. central trade break retrieval).

3. Streamable HTTP (2026-07-28 revision):
   - Mechanism: Unified bidirectional streaming over HTTP/2 or HTTP/3 chunked transfers without requiring separate SSE and POST channels.
   - Pros: Cleaner connection pooling, lower latency, native support in modern cloud API gateways (such as Azure API Management).
   - Bank Use Case: Cloud-native GenAI platforms routing requests through an enterprise API gateway.

## Likely follow-ups

- Why must an MCP server writing to stdio never use standard `print()` statements for debugging?
- How should a corporate proxy that buffers HTTP streaming responses be configured for SSE?

---

[← Q0603](../../batch_07_mcp_a2a_skills_assistants/0603_json_rpc_2_0_framing_in_mcp/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0605 →](../../batch_07_mcp_a2a_skills_assistants/0605_mcp_2026_07_28_stateless_revision/README.md)

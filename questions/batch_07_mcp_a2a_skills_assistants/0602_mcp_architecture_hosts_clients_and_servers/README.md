# Q0602 · MCP architecture: hosts, clients and servers

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Easy |

## Question

Describe the three distinct roles in the MCP architecture (Host, Client, Server) and how they communicate.

## Answer

The Model Context Protocol defines three distinct architectural components:

1. Host:
   - The user-facing container or runtime application (e.g. enterprise desktop assistant, IDE, or agent orchestration service).
   - Responsible for application lifecycle, UI rendering, user security permissions, and coordinating one or more MCP clients.
2. Client:
   - An internal protocol adapter maintained by the host.
   - Maintains a 1:1 connection with a single MCP server.
   - Negotiates capabilities during initialization, translates host queries into JSON-RPC 2.0 messages, and parses server responses.
   - A host often manages multiple clients concurrently (e.g. one client connected to a Git MCP server, another to a PostgreSQL server).
3. Server:
   - An independent process or remote service providing context, tools, and prompts.
   - Does not initiate connections or interact directly with the LLM; it solely responds to requests and emits notifications over its transport.

Communication follows JSON-RPC 2.0: clients issue requests (with an `id`) or notifications (without an `id`), and servers respond with matching `id` results or errors.

## Likely follow-ups

- Can an MCP server initiate a request to the client?
- How does a host decide which server should execute a requested tool call?

---

[← Q0601](../../batch_07_mcp_a2a_skills_assistants/0601_what_the_model_context_protocol_is_and_why_it_exists/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0603 →](../../batch_07_mcp_a2a_skills_assistants/0603_json_rpc_2_0_framing_in_mcp/README.md)

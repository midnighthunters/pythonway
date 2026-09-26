# Q0607 · Capability negotiation in MCP

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

What capabilities can an MCP client and server negotiate during initialization, and how do they impact runtime behavior?

## Answer

Capability negotiation allows clients and servers to advertise supported features so neither party sends unsupported requests.

Server capabilities:
- `tools`: Advertises tool support. Sub-capability `listChanged: true` indicates the server will push `notifications/tools/list_changed` when tools are added or removed.
- `resources`: Advertises read-only resources. Sub-capabilities include `subscribe: true` (client can subscribe to URIs) and `listChanged: true`.
- `prompts`: Advertises reusable prompt templates, with optional `listChanged: true`.
- `logging`: Indicates the server can emit `notifications/message` log events with structured severity levels (debug, info, warning, error).

Client capabilities:
- `sampling`: Crucial feature where the *server* can request LLM completions back from the *client* (via `sampling/createMessage`). If the client does not advertise `sampling`, the server cannot invoke an LLM.
- `roots`: Client can expose workspace filesystem roots (`roots/list`) so the server knows which directories it is permitted to inspect.
- `experimental`: Dictionary of non-standard vendor extensions.

If a server does not declare `prompts`, a compliant client must not call `prompts/list` or `prompts/get`.

## Likely follow-ups

- What is the security implication of a client granting the `sampling` capability to an untrusted MCP server?
- How does `roots/list_changed` allow a client to dynamically restrict filesystem boundaries?

---

[← Q0606](../../batch_07_mcp_a2a_skills_assistants/0606_mcp_initialize_lifecycle_and_handshake/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0608 →](../../batch_07_mcp_a2a_skills_assistants/0608_mcp_ping_and_liveness_detection/README.md)

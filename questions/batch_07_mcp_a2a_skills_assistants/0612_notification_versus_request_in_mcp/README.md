# Q0612 · Notification versus Request in MCP

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Easy |

## Question

What is the semantic difference between a Request and a Notification in MCP? Give three examples of standard MCP notifications.

## Answer

Semantic differences:
1. `id` field: Requests have an `id` (int or str); notifications omit the `id` field entirely.
2. Response expectation: Requests require the receiver to return a Response (result or error) matching the `id`. Notifications must NEVER be replied to.
3. Flow direction: Requests are usually client-to-server (though clients supporting `sampling` can receive requests from servers). Notifications can be sent in either direction at any time after initialization.

Standard MCP Notifications:
1. `notifications/initialized`: Sent by the client to signal that the client has received server capabilities and is ready to begin operations.
2. `notifications/tools/list_changed`: Sent by the server to inform the client that available tools have been added, modified, or removed. The client should re-query `tools/list`.
3. `notifications/resources/updated`: Sent by the server when a resource that the client subscribed to has changed, containing the URI that was updated.
4. `notifications/message`: Emitted by the server for logging / telemetry back to the client.
5. `notifications/cancelled`: Emitted by the client to advise the server to abort processing an in-flight request.

## Likely follow-ups

- Why does MCP use `notifications/tools/list_changed` instead of sending the updated list of tools directly in the notification?
- What race conditions can occur if a server sends `tools/list_changed` frequently?

---

[← Q0611](../../batch_07_mcp_a2a_skills_assistants/0611_parsing_stdio_stream_into_json_rpc_messages/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0613 →](../../batch_07_mcp_a2a_skills_assistants/0613_handling_client_and_server_cancellations_in_mcp/README.md)

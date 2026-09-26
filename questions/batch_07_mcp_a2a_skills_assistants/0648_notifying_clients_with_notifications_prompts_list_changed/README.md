# Q0648 · Notifying clients with notifications/prompts/list_changed

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Easy |

## Question

When and how should an MCP server emit `notifications/prompts/list_changed`?

## Answer

An MCP server emits `notifications/prompts/list_changed` whenever:
1. A new prompt template is registered.
2. An existing prompt template is deprecated or removed.
3. The arguments or schema of a registered prompt change.

The notification has no `id` and empty `params`:
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/prompts/list_changed"
}
```
Upon receiving this notification, the client invalidates its local prompt cache and re-invokes `prompts/list` if prompt selection menus are actively open.

## Likely follow-ups

- What should a client do if a user is in the middle of filling out arguments for a prompt that gets removed?
- Why does MCP not send delta updates inside the notification payload?

---

[← Q0647](../../batch_07_mcp_a2a_skills_assistants/0647_building_an_in_memory_mcp_prompt_catalog/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0649 →](../../batch_07_mcp_a2a_skills_assistants/0649_multi_server_tool_aggregation_in_an_mcp_client/README.md)

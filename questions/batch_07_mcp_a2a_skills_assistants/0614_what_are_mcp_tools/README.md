# Q0614 · What are MCP Tools

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Easy |

## Question

What are MCP Tools, and how do their capabilities and execution model differ from standard OpenAPI endpoints or local Python functions?

## Answer

MCP Tools are executable endpoints exposed by an MCP server that an LLM can discover, inspect, and invoke during reasoning loops.

Key attributes:
1. Self-describing schema: Every tool declares `name`, `description`, and `inputSchema` formatted as standard JSON Schema. The model uses the description and schema to decide when and how to call the tool.
2. Controlled execution: Tools are invoked by the MCP client via the `tools/call` method with specific arguments. The server runs the code and returns structured content blocks.
3. Content results: Tool output is returned as a list of content items (text blocks, base64 images, or embedded resource representations) rather than arbitrary raw byte streams.
4. Error differentiation: Tools can signal failure via `isError: true` without failing the JSON-RPC transport connection.

Differences from OpenAPI / REST:
- Dynamic discovery: The host queries `tools/list` over the active connection and can subscribe to dynamic changes via `notifications/tools/list_changed`.
- Transport-agnostic: A tool can run locally via stdio or remotely via HTTP without rewriting client tool invocation code.
- Human-in-the-loop: MCP clients commonly hook approval prompts right before issuing `tools/call`.

## Likely follow-ups

- Why is the `description` field of an MCP tool critical for agent performance?
- What are the risks of exposing high-privilege tools without client-side confirmation?

---

[← Q0613](../../batch_07_mcp_a2a_skills_assistants/0613_handling_client_and_server_cancellations_in_mcp/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0615 →](../../batch_07_mcp_a2a_skills_assistants/0615_designing_a_tool_schema_with_json_schema/README.md)

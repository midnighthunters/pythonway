# Q0619 · Reporting tool errors: isError flag versus JSON-RPC error

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

What is the architectural difference between setting `isError: true` in a tool result versus returning a JSON-RPC error frame? When must an enterprise engineer use each?

## Answer

In MCP, error reporting occurs at two distinct layers:

1. Protocol / Transport Level (JSON-RPC Error Frame):
   - Example: Method does not exist (`-32601`), invalid JSON payload (`-32700`), unparseable parameters (`-32602`), server internal crash before tool execution (`-32603`).
   - Effect: Breaks the tool-calling loop. The client/host handles the failure as a systemic communication fault. The LLM typically does not see the error payload; the orchestrator either aborts or retries the connection.

2. Application / Tool Execution Level (`isError: true` inside Result):
   - Example: SQL query failed due to a syntax error; account number not found in core banking database; external API returned HTTP 404 or 403; rate limit exceeded on upstream system.
   - Effect: The tool call completes successfully from a protocol perspective. The JSON-RPC response contains `"result": {"content": [{"type": "text", "text": "Account ACC-999 not found in database"}], "isError": true}`.
   - Benefit: The LLM receives the error text directly as observation context. This allows autonomous agents to self-correct (e.g. "I see account ACC-999 was not found; let me search by customer name instead").

Rule of Thumb: If the model can potentially understand, learn from, or recover from the message, use `isError: true`. If the server or protocol is broken, return a JSON-RPC error.

## Likely follow-ups

- Why should a database timeout be reported as `isError: true` to an agent?
- How can an orchestrator prevent an agent from looping indefinitely when a tool continually returns `isError: true`?

---

[← Q0618](../../batch_07_mcp_a2a_skills_assistants/0618_tool_response_structure_text_image_and_resource_contents/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0620 →](../../batch_07_mcp_a2a_skills_assistants/0620_validating_tool_arguments_against_pydantic_models/README.md)

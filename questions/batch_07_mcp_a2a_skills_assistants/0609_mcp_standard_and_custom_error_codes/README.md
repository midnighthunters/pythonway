# Q0609 · MCP standard and custom error codes

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Medium |

## Question

What error codes are defined in JSON-RPC 2.0 and MCP, and how should an MCP server structure error responses?

## Answer

MCP uses standard JSON-RPC 2.0 error codes alongside protocol-specific codes in the reserved range -32000 to -32099:

Standard JSON-RPC 2.0 codes:
- `-32700`: Parse error (invalid JSON received by the server).
- `-32600`: Invalid Request (JSON sent is not a valid JSON-RPC 2.0 request).
- `-32601`: Method not found (requested method does not exist on the server).
- `-32602`: Invalid params (parameters fail schema validation or are missing).
- `-32603`: Internal error (uncaught server exception).

MCP-specific error codes:
- `-32002`: Server not initialized (client attempted an operation before `initialize` handshake completed).
- `-32001`: Request cancelled (request was cancelled by a client notification).

Error structure:
```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "error": {
    "code": -32602,
    "message": "Invalid parameters for tool 'calc_risk'",
    "data": {"missing": ["portfolio_id"]}
  }
}
```
Application-level errors inside tools (e.g. database query returned 0 rows) should generally NOT return JSON-RPC errors; they should return successful tool results with `isError: true` so the model can inspect the error message and recover.

## Likely follow-ups

- Why should tool execution errors return `isError: true` rather than JSON-RPC code -32603?
- Under what circumstances should an SQL syntax error be a JSON-RPC error versus a tool result error?

---

[← Q0608](../../batch_07_mcp_a2a_skills_assistants/0608_mcp_ping_and_liveness_detection/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0610 →](../../batch_07_mcp_a2a_skills_assistants/0610_building_a_minimal_json_rpc_2_0_message_parser_and_builder/README.md)

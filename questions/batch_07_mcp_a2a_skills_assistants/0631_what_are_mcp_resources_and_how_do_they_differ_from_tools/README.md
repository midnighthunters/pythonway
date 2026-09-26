# Q0631 · What are MCP Resources and how do they differ from Tools

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Easy |

## Question

What are MCP Resources, and how do they differ from MCP Tools in purpose, execution model, and security semantics?

## Answer

MCP Resources represent passive, read-only data items exposed by an MCP server to provide context to the LLM or user.

Comparison:
1. Purpose:
   - Tools: Active actions (executing code, modifying records, invoking APIs, running calculations).
   - Resources: Contextual grounding data (configuration files, database schemas, application logs, documentation, policy manuals).
2. Invocation & Control:
   - Tools: Invoked dynamically by the LLM via `tools/call`. The model decides when to execute them and supplies input arguments.
   - Resources: Read explicitly by the client or host via `resources/read` using standard URIs. The host or user can attach resources directly to context windows.
3. Side Effects:
   - Tools: Frequently have side effects (sending emails, placing trades, writing files).
   - Resources: Purely read-only and idempotent. Reading a resource must never cause state mutations.
4. Security:
   - Tools: Require parameter validation, sandboxing, and frequently human-in-the-loop approval.
   - Resources: Governed by standard Read Access Control (RBAC), URI path validation, and content length caps.

## Likely follow-ups

- Can an LLM directly request to read an MCP resource during reasoning?
- How does an MCP resource differ from a document retrieved from a vector database in RAG?

---

[← Q0630](../../batch_07_mcp_a2a_skills_assistants/0630_converting_langchain_tools_to_mcp_tool_definitions/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0632 →](../../batch_07_mcp_a2a_skills_assistants/0632_mcp_resource_uri_schemes_and_structure/README.md)

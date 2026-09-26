# Q0601 · What the Model Context Protocol is and why it exists

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP foundations | Easy |

## Question

What is the Model Context Protocol (MCP), and what architectural problem does it solve for enterprise LLM applications?

## Answer

The Model Context Protocol (MCP) is an open, standardised protocol developed by Anthropic (and maintained as an open standard) that connects LLM applications (hosts/clients) to external data sources, tools, and prompts (servers) over a uniform JSON-RPC 2.0 interface.

Before MCP, integrating an LLM application with enterprise systems (databases, Git repositories, ticketing systems, internal APIs) required writing bespoke tool-calling wrappers for every model provider and application framework. This created an M×N integration problem where M agent frameworks had to build custom adapters for N enterprise data sources.

MCP standardises this relationship:
- Host/Client: The LLM application or IDE (such as Claude Desktop, an enterprise chat UI, or a LangGraph orchestrator) that controls the model and decides when to inspect resources or invoke tools.
- Server: A lightweight service exposing three primary primitives:
  1. Tools: Executable functions with JSON Schema parameters that the model can invoke (with human approval if needed).
  2. Resources: Read-only data items identified by URIs (files, database rows, logs, API payloads) that provide contextual grounding.
  3. Prompts: Pre-defined prompt templates and conversational workflows that users or agents can load.

By separating model orchestration from tool implementation, an enterprise can build and secure an internal database MCP server once, and any authorized client or agent can leverage it.

## Likely follow-ups

- How does MCP differ from OpenAPI or REST specifications for function calling?
- When would you build an MCP server rather than writing a direct Python tool in LangGraph?

---

[← Q0600](../../batch_06_langgraph_langchain/0600_build_a_small_agent_end_to_end_in_an_interview/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0602 →](../../batch_07_mcp_a2a_skills_assistants/0602_mcp_architecture_hosts_clients_and_servers/README.md)

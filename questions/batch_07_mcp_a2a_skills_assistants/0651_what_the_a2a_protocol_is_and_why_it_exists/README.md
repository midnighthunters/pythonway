# Q0651 · What the A2A protocol is and why it exists

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A foundations | Easy |

## Question

What is the Agent-to-Agent (A2A) protocol v1.0, and what problem does it solve in enterprise multi-agent systems?

## Answer

The Agent-to-Agent (A2A) protocol is an open standard designed for secure, autonomous, task-oriented communication between independent AI agents.

While MCP standardizes how an agent talks to tools and data sources within its own execution boundary, A2A standardizes how independent agents across different systems, teams, or organizations discover each other, delegate complex multi-step tasks, stream progress, exchange artifacts, and reach consensus.

Why A2A exists:
1. Heterogeneous agent stacks: One team may build an agent with LangGraph in Python; another with AutoGen, Semantic Kernel in C#, or an autonomous LLM service in Go. A2A provides an agnostic HTTP/SSE and JSON-RPC protocol boundary.
2. Long-running, asynchronous tasks: Unlike quick synchronous tool calls, agent delegation often takes minutes or hours (e.g. conducting financial due diligence or reconciling batch trade breaks). A2A models stateful tasks with intermediate progress reporting.
3. Declarative discovery: Agents publish standardized "Agent Cards" describing their identity, capabilities, input/output schemas, and authentication requirements.
4. Human-in-the-loop across boundaries: An agent can pause and signal `needs_input` back to the calling agent or human supervisor.

## Likely follow-ups

- Why couldn't HTTP REST APIs be used directly instead of creating A2A?
- How does A2A prevent runaway delegation loops between autonomous agents?

---

[← Q0650](../../batch_07_mcp_a2a_skills_assistants/0650_namespacing_tools_across_multiple_mcp_servers/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0652 →](../../batch_07_mcp_a2a_skills_assistants/0652_mcp_versus_a2a_comparative_architectural_analysis/README.md)

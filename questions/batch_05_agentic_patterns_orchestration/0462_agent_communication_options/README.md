# Q0462 · Agent communication options

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Protocols | Medium |

## Question

Compare the ways agents and tools communicate: in-process function or tool calls, in-framework handoffs, MCP, A2A and message queues. When would you use each?

## Answer

- In-process tool calls: the agent calls Python functions directly. It is fastest and simplest, suited to tools owned by the same team and deployed together.
- In-framework handoffs and sub-graphs (for example LangGraph): multiple agents in one runtime with shared state and checkpointing. Good for tightly coupled workflows owned by one team.
- MCP (Model Context Protocol): a standard way for an agent host to discover and call tools, resources and prompts exposed by separate servers. Use it to share tools across many agents and teams, with auth, discovery and versioning. The 2026-07-28 revision makes it stateless, per-request.
- A2A (Agent2Agent): a standard for one agent to delegate a task to another, independently built agent (Agent Cards for discovery, tasks with lifecycle states, streaming and push notifications). Use it across team or vendor boundaries where the other side is an agent, not a tool.
- Message queues and events (Kafka, SQS, Service Bus): asynchronous, decoupled, durable triggers and results. Good for long-running and background work, and for integrating with existing enterprise systems.

A platform typically uses all of them: MCP for the tool ecosystem, A2A for cross-team agents, queues for durability, and in-process calls inside each agent.

## Likely follow-ups

- When would you expose an agent via A2A rather than as an MCP tool?

---

[← Q0461](../../batch_05_agentic_patterns_orchestration/0461_blackboard_architecture/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0463 →](../../batch_05_agentic_patterns_orchestration/0463_choosing_an_agent_framework/README.md)

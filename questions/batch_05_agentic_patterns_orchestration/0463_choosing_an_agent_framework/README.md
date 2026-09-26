# Q0463 · Choosing an agent framework

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Frameworks | Medium |

## Question

How would you evaluate agent frameworks (LangGraph, LangChain agents, OpenAI Agents SDK, Semantic Kernel, AutoGen-style libraries, cloud-managed agents such as Bedrock AgentCore) for an enterprise platform?

## Answer

Criteria:
- Control and transparency: explicit graphs and state (auditable, testable) versus opaque loops.
- Durability: checkpointing, resume, human-in-the-loop interrupts and long-running support.
- Model agnosticism: works across Azure OpenAI, Bedrock and self-hosted models through the platform gateway.
- Tooling standards: MCP client support, A2A support, and structured outputs.
- Streaming and UX: token, event and state streaming to front ends.
- Observability: tracing (OpenTelemetry or LangSmith), and hooks for guardrails and evaluation.
- Deployment and operations: runs in your own infrastructure (containers, Kubernetes), scaling, versioning of in-flight runs, and security review of the dependencies.
- Maturity: API stability (for example LangChain and LangGraph at 1.x), community, vendor support, and licence.
- Team fit: Python and TypeScript support, learning curve.

A common enterprise answer: LangGraph for orchestration (explicit and durable), MCP for tools, A2A for inter-agent calls, a platform LLM gateway, and managed runtimes where they meet the controls. Prototype the hardest workflow in two options before standardising.

## Likely follow-ups

- What's the risk of adopting a fast-moving framework in a bank, and how do you mitigate it?

---

[← Q0462](../../batch_05_agentic_patterns_orchestration/0462_agent_communication_options/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0464 →](../../batch_05_agentic_patterns_orchestration/0464_stateless_versus_stateful_agent_services/README.md)

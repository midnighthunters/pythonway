# Q0499 · Design an agentic orchestration platform for LLM Suite

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | System design | Hard |

## Question

Design the shared agent runtime for LLM Suite, so application teams can build agents that are secure, reliable and observable by default.

## Answer

Core services:
1. Agent runtime: a graph-based orchestration (for example LangGraph) running on stateless workers with durable checkpoints (Postgres), interrupts for human-in-the-loop, streaming of events, and deadline and budget enforcement.
2. LLM gateway: model routing across Azure OpenAI, Bedrock and self-hosted models, quotas, retries and fallbacks, prompt caching, cost metering and content filtering.
3. Tool plane: an MCP gateway fronting approved MCP servers (a registry with owners, scopes, versions and risk tiers), per-request authorisation with on-behalf-of tokens, argument validation, rate limits and audit.
4. Agent plane: A2A endpoints for cross-team agents (Agent Cards in a registry, signed cards, task lifecycle tracking).
5. Policy and approvals: a policy engine for tool calls (auto, approve or deny), an approval service with four-eyes rules, and notifications.
6. Memory service: per-user and per-tenant stores with namespaces, inspection and deletion APIs, retention and poisoning controls.
7. Observability and evaluation: OpenTelemetry tracing across agents, tools and models, evaluation pipelines and gates, replay tooling and dashboards.
8. Governance: an agent registry (owners, versions, risk tier, model-risk status), change management, kill switches per agent and tenant.

Developer experience: templates and SDKs, a local fake stack (fake LLM, simulated tools), CI evaluation templates, and paved-road defaults. Teams write the graph and tools, and the platform provides the controls.

## Likely follow-ups

- What would you ship in the first quarter, and what would wait?
- Which platform controls should be impossible for teams to disable?

---

[← Q0498](../../batch_05_agentic_patterns_orchestration/0498_tamper_evident_audit_trail_for_agent_actions/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0500 →](../../batch_05_agentic_patterns_orchestration/0500_whiteboard_disruption_recovery_with_cooperating_agents/README.md)

# Q0696 · Zero-trust architecture for enterprise MCP and A2A networks

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP and A2A security | Hard |

## Question

Design a Zero-Trust security architecture for an enterprise deployment of hundreds of internal MCP servers and A2A agents.

## Answer

In a Zero-Trust model, no agent, client, or tool server is trusted simply because it resides inside the corporate network perimeter.

Zero-Trust Principles for MCP & A2A:
1. Mutual TLS (mTLS) Everywhere: Every connection between hosts, MCP servers, and A2A agents requires cryptographic identity verification via internal PKI certificates.
2. Short-Lived OAuth 2.0 / JWT Tokens: Requests carry scoped bearer tokens specifying exact client identity, user delegation chain, and permitted tool scopes (e.g. `scope: "tools:market_data:read"`).
3. Least Privilege & Role-Based Access: Agents only discover and execute tools explicitly permitted for their operational profile and the calling user's entitlements.
4. Immutable Audit Logs: Every tool call, parameter set, and response payload is logged to an append-only compliance data lake (e.g. Kafka to Snowflake/S3) for regulatory review.
5. Network Microsegmentation: Kubernetes network policies isolate MCP tool pods so they can only connect to authorized database backends, blocking lateral movement.

## Likely follow-ups

- How do you handle token exchange when Agent A delegates a task to Agent B on behalf of User C?
- What are the performance overheads of verifying JWT signatures on every tool invocation?

---

[← Q0695](../../batch_07_mcp_a2a_skills_assistants/0695_privacy_boundaries_and_sensitive_personal_data_isolation/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0697 →](../../batch_07_mcp_a2a_skills_assistants/0697_preventing_prompt_injection_across_a2a_agent_boundaries/README.md)

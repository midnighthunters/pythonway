# Q0632 · MCP resource URI schemes and structure

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Medium |

## Question

Explain the structure of MCP Resource URIs and design an enterprise URI scheme for bank financial data.

## Answer

MCP Resources are addressed using Uniform Resource Identifiers (URIs) as defined by RFC 3986. Every resource URI consists of:
`scheme://authority/path?query#fragment`

Enterprise Scheme Design for Bank Data:
- `file:///workspace/policies/credit_risk.md`: Local files exposed to the agent.
- `postgres://core-db.internal/trades/2026-09-26`: Direct database table or record representations.
- `jpmc-risk://accounts/{account_id}/positions`: Dynamic internal risk service representations.
- `logs://prod-cluster/services/order-gateway/today`: Centralized log streams.

Attributes of good resource URIs:
- Deterministic: Identical URIs should return the same logical resource entity over time.
- Hierarchical: Enables wildcard subscriptions (e.g. subscribing to `jpmc-risk://accounts/LDN-101/*`).
- MIME Typed: Every URI returned by `resources/list` must declare its `mimeType` (e.g. `text/plain`, `application/json`, `application/pdf`).

## Likely follow-ups

- Why should confidential account credentials never be embedded inside resource URI query parameters?
- How do resource templates allow servers to expose parameterized URI patterns?

---

[← Q0631](../../batch_07_mcp_a2a_skills_assistants/0631_what_are_mcp_resources_and_how_do_they_differ_from_tools/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0633 →](../../batch_07_mcp_a2a_skills_assistants/0633_listing_resources_with_resources_list_and_pagination/README.md)

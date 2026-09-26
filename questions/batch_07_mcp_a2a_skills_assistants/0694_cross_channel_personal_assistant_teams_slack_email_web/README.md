# Q0694 · Cross-channel personal assistant: Teams, Slack, Email, Web

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

How do you design an assistant architecture that allows a user to interact seamlessly across Teams, email, and web chat while sharing a single unified memory and state?

## Answer

A cross-channel assistant decouples the channel presentation layer from the central assistant core:

Architecture:
1. Channel Adapters: Lightweight ingress gateways (Bot Framework for Teams, Slack Bolt SDK, Exchange Web Services for Email, FastAPI WebSocket for Web) translate native channel payloads into a canonical message format.
2. Unified Identity Mapping: Entra ID / corporate email address links channel-specific user IDs (e.g. Slack user `U123` -> corporate `alice@jpmc.com`).
3. Central Conversation & Memory Store: Redis/PostgreSQL keyed by canonical user ID, not channel ID.
4. Channel-Specific Rendering: The core outputs canonical markdown and action cards. The adapter formats them into Teams Adaptive Cards, Slack Block Kit, or HTML email.

## Likely follow-ups

- How do you handle channel limitations (e.g. email has high latency and no streaming SSE)?
- How do security boundaries differ between an internal web portal and an email channel?

---

[← Q0693](../../batch_07_mcp_a2a_skills_assistants/0693_handling_multi_turn_conversational_context_drift/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0695 →](../../batch_07_mcp_a2a_skills_assistants/0695_privacy_boundaries_and_sensitive_personal_data_isolation/README.md)

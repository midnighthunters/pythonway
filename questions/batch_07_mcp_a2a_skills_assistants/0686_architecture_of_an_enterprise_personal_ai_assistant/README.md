# Q0686 · Architecture of an enterprise Personal AI Assistant

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

Describe the high-level architecture of an enterprise Personal AI Assistant (e.g. JPMC LLM Suite Personal Assistant) integrating chat, tools, memory, and enterprise connectors.

## Answer

An enterprise Personal AI Assistant coordinates multiple capabilities while operating within corporate security boundaries:

Core Architectural Layers:
1. Client / Presentation Layer:
   - Web Chat UI, Outlook add-in, Teams/Slack bot, or desktop application.
   - Handles streaming text, structured cards, user approval modals, and voice input.
2. Gateway & Security Firewall:
   - Authentication (Entra ID / Kerberos SSO), RBAC, PII redaction, input prompt injection filters.
3. Orchestration Engine (e.g. LangGraph / ReAct):
   - Manages dialog state, conversation history pruning, and multi-turn reasoning loops.
4. Layered Memory System:
   - Working memory (active context window).
   - Episodic memory (vectorized conversation archives).
   - Semantic profile store (user preferences, frequently referenced counterparties, working group).
5. MCP & A2A Integration Mesh:
   - Connects to internal tools via MCP (SQL database queries, Jira, Git, corporate directory).
   - Delegates complex workflows via A2A to backend agent swarms (Risk Agent, Compliance Agent).

## Likely follow-ups

- How does a personal assistant differ from a generic chatbot?
- How is tenant data isolation enforced across personal assistant instances?

---

[← Q0685](../../batch_07_mcp_a2a_skills_assistants/0685_implementing_a_dynamic_skill_registry_and_loader/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0687 →](../../batch_07_mcp_a2a_skills_assistants/0687_layered_memory_in_personal_assistants_working_episodic/README.md)

# Q0641 · What are MCP Prompts and use cases

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP prompts | Easy |

## Question

What are MCP Prompts, and how do they differ from system prompts or prompt templates stored inside the client application?

## Answer

MCP Prompts are server-defined, reusable conversational templates and workflows that clients can discover and load dynamically.

Key characteristics:
1. Server-Side Definition:
   - Instead of hardcoding prompts inside the client application or IDE, the server exposes prompt definitions via `prompts/list` and fulfills them via `prompts/get`.
   - Allows domain teams (e.g. risk desk, compliance, equities) to update and version prompt engineering instructions centrally without requiring client code releases.
2. Parameterized:
   - Prompts declare required and optional arguments (e.g. `portfolio_id`, `analysis_depth`).
   - The client UI can inspect arguments and prompt the user to fill in values.
3. Multi-Turn / Multi-Role:
   - Fulfilling a prompt returns a sequence of messages with assigned roles (`user` or `assistant`), allowing few-shot examples or system priming.
4. Embedded Resources:
   - Prompts can directly embed server resources (e.g. attaching the latest credit policy document directly to the prompt context).

## Likely follow-ups

- How does an MCP prompt enhance user experience in an enterprise chat assistant?
- Can an LLM autonomously invoke an MCP prompt, or are prompts user-initiated?

---

[← Q0640](../../batch_07_mcp_a2a_skills_assistants/0640_access_control_on_sensitive_resources_by_uri_pattern/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0642 →](../../batch_07_mcp_a2a_skills_assistants/0642_listing_prompt_templates_with_prompts_list/README.md)

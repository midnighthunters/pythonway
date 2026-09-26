# Q0693 · Handling multi-turn conversational context drift

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

When a user changes the topic mid-conversation (e.g. from analyzing equity risk to drafting an email), how does the assistant avoid context confusion while preserving previous state?

## Answer

Techniques to handle context drift:
1. Topic Drift Detection: An intent classifier or LLM turn-evaluator detects that the new prompt shares zero semantic overlap with the current task.
2. Branching / Thread Stacking: Rather than discarding the previous task, the assistant pushes the active state onto a thread stack. The user can return later ("Back to the equity risk analysis").
3. Selective Context Pruning: Isolate specialized tools and system prompts to active sub-threads, preventing unrelated tools from cluttering the context window.
4. Explicit Clarification: If ambiguity arises ("Proceed with it"), the assistant explicitly resolves pronouns against the current versus prior thread.

## Likely follow-ups

- How does LangGraph's subgraph or checkpoint fork mechanism support thread switching?
- When should the assistant ask: "Should I close our previous discussion?"

---

[← Q0692](../../batch_07_mcp_a2a_skills_assistants/0692_human_in_the_loop_confirmation_ux_for_personal_assistant/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0694 →](../../batch_07_mcp_a2a_skills_assistants/0694_cross_channel_personal_assistant_teams_slack_email_web/README.md)

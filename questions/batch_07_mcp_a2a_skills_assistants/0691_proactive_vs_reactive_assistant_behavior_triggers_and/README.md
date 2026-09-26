# Q0691 · Proactive vs reactive assistant behavior: triggers and schedules

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

How does a personal AI assistant balance proactive actions (e.g. morning briefings, trade break alerts) with reactive conversation? What architectures enable proactive triggers?

## Answer

Reactive assistants only act when a user types a prompt. Proactive assistants initiate interactions based on external events or schedules.

Architecture for Proactivity:
1. Event-Driven Triggers:
   - Webhooks from enterprise messaging queues (Kafka, RabbitMQ) for critical events (e.g. margin call breached, trade rejected).
   - The assistant filters events through user relevance models before interrupting.
2. Scheduled Cron Jobs:
   - Morning briefing daemon generates market overviews at 07:30 AM based on the user's portfolio watchlist.
3. Attention Management & Politeness Rules:
   - Priority scoring: Low-urgency items are batched into a daily digest; high-urgency compliance alerts trigger immediate desktop push notifications.
   - Do Not Disturb (DND) awareness: Suppress notifications during active meetings or outside trading desk hours.

## Likely follow-ups

- What is the danger of "alert fatigue" caused by an overly proactive AI assistant?
- How should user feedback ("Don't notify me about this again") tune the proactive filter?

---

[← Q0690](../../batch_07_mcp_a2a_skills_assistants/0690_calendar_and_meeting_management_via_personal_assistant/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0692 →](../../batch_07_mcp_a2a_skills_assistants/0692_human_in_the_loop_confirmation_ux_for_personal_assistant/README.md)

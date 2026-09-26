# Q0598 · Design a LangGraph personal assistant

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | System design | Hard |

## Question

Sketch a LangGraph architecture for an employee's personal assistant (email, calendar, documents, expenses) with memory and approvals.

## Answer

- Entry graph: `load_context` (the user profile from the runtime context, and relevant memories from the Store via semantic search), then `route` (intent classification with an enum), then one of several skill subgraphs.
- Skill subgraphs (each a `create_agent` or custom graph with a scoped tool set): `inbox_triage` (read and summarise, draft replies), `scheduling` (find slots, propose, book after approval), `documents` (RAG over the user's accessible documents), `expenses` (extract receipts, draft the claim, submit after approval).
- Approvals: HITL middleware or an `interrupt()` before send, book or submit tools. The approval card shows the concrete action.
- Memory: a `save_memories` node after each turn extracts preferences from the user's own messages only and writes them to the Store namespace `(tenant, user)`. A memory UI lets the user view and delete them.
- Background: scheduled runs (a morning briefing) and event triggers (a new calendar invite) as background runs on per-user threads, with notifications instead of actions.
- Safety: untrusted email and document content is never granted tool authority, there's an input guard for injection patterns, the output is sanitised, per-user rate limits apply, and every action is audited.
- Persistence: a Postgres checkpointer (threads per conversation) and the Store for long-term memory, both encrypted and covered by retention and deletion.

## Likely follow-ups

- How would you stop a malicious email from triggering the scheduling skill?

---

[← Q0597](../../batch_06_langgraph_langchain/0597_design_a_langgraph_trade_break_agent/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0599 →](../../batch_06_langgraph_langchain/0599_rebooking_workflow_as_a_langgraph_graph/README.md)
